START_BYTE = 0xAA

# Command IDs
CMD_PING = 0x01
CMD_SELECT_HEAD = 0x02
CMD_MOVE_ARM = 0x03
CMD_LOCK = 0x04
CMD_RELEASE = 0x05
CMD_SET_LED = 0x06

def build_packet(head_id, command, data=b""):
    payload = bytes([head_id, command]) + data
    checksum = sum(payload) & 0xFF
    return bytes([START_BYTE, len(payload)]) + payload + bytes([checksum])

def parse_packet(raw):
    if len(raw) < 4 or raw[0] != START_BYTE:
        return None
    length = raw[1]
    if len(raw) < 3 + length:
        return None
    payload = raw[2:2 + length]
    checksum = raw[2 + length]
    if sum(payload) & 0xFF != checksum:
        return None
    return {"head_id": payload[0], "command": payload[1], "data": payload[2:]}
