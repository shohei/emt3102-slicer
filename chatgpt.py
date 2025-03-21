import struct

def read_binary_stl(filename):
    with open(filename, "rb") as f:
        # 80バイトのヘッダーをスキップ
        header = f.read(80)
        print("Header:", header.decode(errors="ignore"))

        # 4バイトの三角形数を取得
        num_triangles = struct.unpack("<I", f.read(4))[0]
        print("Number of triangles:", num_triangles)

        triangles = []

        for _ in range(num_triangles):
            # 1つの三角形のデータ（50バイト）
            data = f.read(50)

            # 法線ベクトル (3 x float32)
            normal = struct.unpack("<fff", data[0:12])

            # 3つの頂点座標 (3 x (3 x float32))
            v1 = struct.unpack("<fff", data[12:24])
            v2 = struct.unpack("<fff", data[24:36])
            v3 = struct.unpack("<fff", data[36:48])

            # 2バイトの属性バイト数（無視する）
            attr_byte_count = struct.unpack("<H", data[48:50])[0]

            triangles.append((normal, v1, v2, v3))

        return triangles

# 例：STLファイルを読み込んで表示
stl_file = "your_file.stl"
triangles = read_binary_stl(stl_file)

# 最初の三角形を表示
if triangles:
    print("First triangle:")
    print("  Normal:", triangles[0][0])
    print("  Vertex 1:", triangles[0][1])
    print("  Vertex 2:", triangles[0][2])
    print("  Vertex 3:", triangles[0][3])
