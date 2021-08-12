# Copyright 2011-2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
An L2 learning switch.

It is derived from one written live for an SDN crash course.
It is somwhat similar to NOX's pyswitch in that it installs
exact-match rules for each flow.
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str, str_to_dpid
from pox.lib.util import str_to_bool
import time

log = core.getLogger()

# We don't want to flood immediately when a switch connects.
# Can be overriden on commandline.
_flood_delay = 0

class LearningSwitch (object):
  """
  The learning switch "brain" associated with a single OpenFlow switch.

  Cuando vemos un PAQUETE, nos gustaria que saliera por un puerto que
  lleve eventualmente a un destino. Para lograr esto, construimos una
  tabla que mapea direcciones a puertos.

  Se llena la tabla observando el trafico de paquetes. Cuando se ve un paquete
  desde una fuente de origen llegando desde un algún puerto, se sabe
  que esa fuente de origen está fuera de tal puerto.

  Cuando se quiere avanzar el tráfico (de paquetes), se observa el
  destino en la tabla. Si no se conoce el puerto, simplemente se envia
  el mensaje a través de todos los puertos excepto del que venia (FLOOD).
  Cuando hay loops, pasan cosas malas

  A grandes rasgos, el algoritmo hace lo siguiente:

  Para cada paquete desde el switch:
  1) Usa la dirección fuente y el puerto de switch para actualizar la tabla de puertos/direcciones
  2) Is transparent = False and either Ethertype is LLDP or the packet's    (Que el paquete sea transparente es que puede reconocerse, supongo)
     destination address is a Bridge Filtered address?
     Yes:
        2a) Drop packet -- don't forward link-local traffic (LLDP, 802.1x)
            DONE
  3) Is destination multicast?      (Direcciones multicast permiten enviar paquetes desde un dispositivo de origen a un grupo de otros dispositivos )
     Yes:
        3a) Flood the packet
            DONE
  4) Port for destination address in our address/port table?        (Si el puerto de destino no está en la tabla, el paquete continúa, ya que aún no llega a donde debe)
     No:
        4a) Flood the packet
            DONE
  5) Is output port the same as input port?         (Si el puerto de output es el mismo de input el paquete no puede moverse, por ende se dropea)
     Yes:
        5a) Drop packet and similar ones for a while
  6) Install flow table entry in the switch so that this    (Instala la entrada de tabla de flujo en el switch de forma en que los paquetes se muevan al puerto apropiado)
     flow goes out the appopriate port
     6a) Send the packet out appropriate port               (PUERTO SE VA AL PUERTO QUE CORRESPONDE)
  """
  def __init__ (self, connection, transparent):
    # Switch we'll be adding L2 learning switch capabilities to
    self.connection = connection
    self.transparent = transparent

    # Our table
    self.macToPort = {}

    # We want to hear PacketIn messages, so we listen
    # to the connection
    connection.addListeners(self)

    # We just use this to know when to log a helpful message
    self.hold_down_expired = _flood_delay == 0

    #log.debug("Initializing LearningSwitch, transparent=%s",
    #          str(self.transparent))

  def _handle_PacketIn (self, event):
    """
    Handle packet in messages from the switch to implement above algorithm.
    """

    packet = event.parsed

    def flood (message = None):
      """ Floods the packet """
      msg = of.ofp_packet_out()
      if time.time() - self.connection.connect_time >= _flood_delay:
        # Only flood if we've been connected for a little while...

        if self.hold_down_expired is False:
          # Oh yes it is!
          self.hold_down_expired = True
          log.info("%s: Flood hold-down expired -- flooding",
              dpid_to_str(event.dpid))

        if message is not None: log.debug(message)
        #log.debug("%i: flood %s -> %s", event.dpid,packet.src,packet.dst)
        # OFPP_FLOOD is optional; on some switches you may need to change
        # this to OFPP_ALL.
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
      else:
        pass
        #log.info("Holding down flood for %s", dpid_to_str(event.dpid))
      msg.data = event.ofp
      msg.in_port = event.port
      self.connection.send(msg)

    def drop (duration = None):
      """
      Drops this packet and optionally installs a flow to continue
      dropping similar ones for a while
      """
      if duration is not None:
        if not isinstance(duration, tuple):
          duration = (duration,duration)
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = duration[0]
        msg.hard_timeout = duration[1]
        msg.buffer_id = event.ofp.buffer_id
        self.connection.send(msg)
      elif event.ofp.buffer_id is not None:
        msg = of.ofp_packet_out()
        msg.buffer_id = event.ofp.buffer_id
        msg.in_port = event.port
        self.connection.send(msg)

    self.macToPort[packet.src] = event.port # 1

    if not self.transparent: # 2
      if packet.type == packet.LLDP_TYPE or packet.dst.isBridgeFiltered():
        drop() # 2a
        return

    if packet.dst.is_multicast:
      flood() # 3a
    else:
      if packet.dst not in self.macToPort: # 4
        flood("Port for %s unknown -- flooding" % (packet.dst,)) # 4a

      else:
        #MAC de salida del mensaje a analizar
        mac_origen = str(packet.src)[-1]

        #MAC de llegada del mensaje a analizar
        mac_destino = str(packet.dst)[-1]

        #Puerto de donde parte el paquete
        puerto = event.port

        try:
            puerto_dst = self.macToPort[packet.dst]
        except:
            drop()


        # HOST 5 y 6 SON HTTP
        # NO HAY COMUNICACION ENTRE HOSTS
        # HOST 1 y 2 SOLO SE PUEDEN COMUNICAR CON HOST 5
        # HOST 3 y 4 SOLO SE PUEDEN COMUNICAR CON HOST 6
        #CUALQUIER OTRO CASO SE DROPEA
        MACS = ["1","2","3","4","5","6","7"]
        #Si el mensaje viene/va desde/hacia un host que no está en la red, se dropea

        if ((mac_origen not in MACS) or (mac_destino not in MACS)):
            log.debug("Paquete rechazado!")
            drop()
            return

        #El paquete parte del switch 1
        elif mac_origen in ["1","2"]:
            log.debug("Paquete del Host 1 o 2")
            #Solo se puede comunicar con el host 5
            if mac_destino == "5":
                if puerto in [2, 4]:
                    log.debug("Está en el switch 1")
                    puerto_dst = 13
                elif puerto == 14:
                    log.debug("Está en el switch 5")
                    if packet.find("tcp") == None:
                        log.debug("Dropeo tcp")
                        drop()
                        return
                    elif packet.find("tcp") and packet.find("tcp").dstport == 80:
                        puerto_dst = 10
                    else:
                        log.debug("dropeo")
                        drop()
                        return


            #Sino, se dropea
            else:
                log.debug("dropeo si mac destino no es 5")
                drop()
                return

        #El paquete parte del switch 2
        elif mac_origen in ["3","4"]:
            print("Paquete del Host 3 o 4")
            #Solo se puede comunicar con el host 6
            if mac_destino == "6":
                if puerto in [6,8]:
                    puerto_dst = 23
                elif puerto == 24:
                    puerto_dst = 13
                elif puerto == 14:
                    log.debug("Está en el switch 5")
                    log.debug("weaita " + str(packet.find("tcp").dstport))
                    if packet.find("tcp") == None:
                        log.debug("dropeo tcp 2")
                        #drop()
                        return
                    elif packet.find("tcp") and packet.find("tcp").dstport == 80:
                        log.debug("Entra el Host 6")
                        puerto_dst = 12
                    else:
                        log.debug("No entra naita al Host 6")
                        drop()
                        return

            #Sino, se dropea
            else:
                log.debug("dropeo si mac destino no es 6")
                drop()
                return
        #Servidores HTTP
        elif mac_origen in ["5", "6"]:
            print("Paquete de los servidores HTTP")
            #El paquete parte del switch 5
            if puerto in [10, 12]:
                puerto_dst = 15
            #Switch 3
            elif puerto == 16:
                if mac_destino  in ["1", "2"]:
                    puerto_dst = 17
                else:
                    puerto_dst = 19
            #Switch 1
            elif puerto == 18:
                if mac_destino == "1":
                    puerto_dst = 2
                elif mac_destino == "2":
                    puerto_dst = 4
            #Switch 4
            elif puerto == 20:
                puerto_dst = 21
            #Switch 2
            elif puerto == 22:
                 if mac_destino == "3":
                     puerto_dst = 6
                 elif mac_destino == "4":
                     puerto_dst = 8
                 elif mac_destino in ["5","6"]:
                     puerto_dst = 23
            else:
                log.debug("dropeo si no hay puerto")
                drop()
                return
        else:
            log.debug("dropeo si no se cumple nada mas")
            drop()
            return

        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, event.port)
        msg.idle_timeout = 10
        msg.hard_timeout = 30
        msg.actions.append(of.ofp_action_output(port = puerto_dst))
        msg.data = event.ofp # 6a
        self.connection.send(msg)


class l2_learning (object):
  """
  Waits for OpenFlow switches to connect and makes them learning switches.
  """
  def __init__ (self, transparent, ignore = None):
    """
    Initialize

    See LearningSwitch for meaning of 'transparent'
    'ignore' is an optional list/set of DPIDs to ignore
    """
    core.openflow.addListeners(self)
    self.transparent = transparent
    self.ignore = set(ignore) if ignore else ()

  def _handle_ConnectionUp (self, event):
    if event.dpid in self.ignore:
      log.debug("Ignoring connection %s" % (event.connection,))
      return
    log.debug("Connection %s" % (event.connection,))
    LearningSwitch(event.connection, self.transparent)


def launch (transparent=False, hold_down=_flood_delay, ignore = None):
  """
  Starts an L2 learning switch.
  """
  try:
    global _flood_delay
    _flood_delay = int(str(hold_down), 10)
    assert _flood_delay >= 0
  except:
    raise RuntimeError("Expected hold-down to be a number")

  if ignore:
    ignore = ignore.replace(',', ' ').split()
    ignore = set(str_to_dpid(dpid) for dpid in ignore)

  core.registerNew(l2_learning, str_to_bool(transparent), ignore)
