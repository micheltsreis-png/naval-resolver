"""Gera ícones PNG para a PWA — âncora naval azul escuro."""
import struct, zlib, math

def make_png(size):
    navy = (10, 35, 66)
    gold  = (201, 168, 76)
    white = (255, 255, 255)
    cx, cy = size // 2, size // 2
    r = cx * 0.88

    rows = []
    for y in range(size):
        row = bytearray()
        for x in range(size):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > r:
                row += bytes([0, 0, 0, 0])
                continue
            # Âncora simplificada
            rel_x = dx / cx
            rel_y = dy / cy
            # Haste vertical
            in_haste = abs(rel_x) < 0.07 and -0.75 < rel_y < 0.55
            # Barra horizontal
            in_barra = abs(rel_y + 0.55) < 0.08 and abs(rel_x) < 0.38
            # Argola
            in_argola = 0.12 < math.sqrt(dx*dx + (dy + cy*0.62)**2) / cx < 0.22
            # Braços curvados
            arm_r = math.sqrt((abs(dx) - cx*0.28)**2 + (dy - cy*0.42)**2)
            in_arms = arm_r / cx < 0.12 and rel_y > 0.25
            if in_haste or in_barra or in_argola or in_arms:
                row += bytes([*white, 255])
            else:
                row += bytes([*navy, 255])
        rows.append(b'\x00' + bytes(row))

    raw = b''.join(rows)
    compressed = zlib.compress(raw)

    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

    ihdr = struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', compressed)
    png += chunk(b'IEND', b'')
    return png

for size, dest in [
    (192, 'public/icons/icon-192.png'),
    (512, 'public/icons/icon-512.png'),
    (180, 'public/apple-touch-icon.png'),
]:
    with open(dest, 'wb') as f:
        f.write(make_png(size))
    print(f'Gerado: {dest}')
