import struct
import numpy as np

def write_stl(vertices, faces, filename="model.stl"):
    
    #hexgen stl sphere
    # -vertices(list of tuples): list of (x, y, z) vertex coordinates
    # -faces(list of tuples): list of (v1_idx, v2_idx, v3_idx) face indices
    # -filename(str)
    with open(filename, 'wb') as f:
        # empty 80 byte header
        f.write(b'\x00' * 80)

        #triangles
        f.write(struct.pack('<I', len(faces)))
        for face in faces:
            v1 = np.array(vertices[face[0]])
            v2 = np.array(vertices[face[1]])
            v3 = np.array(vertices[face[2]])

            normal = np.cross(v2 - v1, v3 - v1)
            normal /= np.linalg.norm(normal)

            #normal vector (3 floats)
            f.write(struct.pack('<3f', *normal))
            #vertices (3 floats * 3)
            f.write(struct.pack('<3f', *v1))
            f.write(struct.pack('<3f', *v2))
            f.write(struct.pack('<3f', *v3))
            #attribute 2 zero bytes
            f.write(b'\x00\x00')

def write_raw(vertices, faces, filename="model.raw"):
    #hexgen .raw format, vertices and faces
    # -vertices(list of tuples): list of (x, y, z) vertex coordinates
    # -faces(list of tuples): list of (v1_idx, v2_idx, v3_idx) face indices
    # -filename(str)
    with open(filename, 'w') as f:
        #header: number of points, faces
        f.write(f"{len(vertices)} {len(faces)}\n")

        #vertex coordinates followed by a 1
        for v in vertices:
            f.write(f"{v[0]} {v[1]} {v[2]} 1\n")

        #face with its 0-based vertex indices
        for face in faces:
            f.write(f"{face[0]} {face[1]} {face[2]}\n")

def gen_sphere(radius=10.0, subdivisions=0):
#sphere mesh
# -radius(float)
# -subdivisions(int), number of face subdivisions
# --returns tuple list of vertices & faces
    t = (1.0 + 5.0**0.5) / 2.0

    vertices = [
        (-1,  t,  0), ( 1,  t,  0), (-1, -t,  0), ( 1, -t,  0),
        ( 0, -1,  t), ( 0,  1,  t), ( 0, -1, -t), ( 0,  1, -t),
        ( t,  0, -1), ( t,  0,  1), (-t,  0, -1), (-t,  0,  1)
    ]

    faces = [
        (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
        (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
        (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
        (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)
    ]

    vertices = [list(np.array(v) / np.linalg.norm(v)) for v in vertices]
    
    vertex_cache = {}

    def get_midpoint(p1_idx, p2_idx):
        key = tuple(sorted((p1_idx, p2_idx)))
        if key in vertex_cache:
            return vertex_cache[key]

        v1 = np.array(vertices[p1_idx])
        v2 = np.array(vertices[p2_idx])
        midpoint = (v1 + v2) / 2.0
        midpoint /= np.linalg.norm(midpoint)
        
        vertices.append(list(midpoint))
        new_idx = len(vertices) - 1
        vertex_cache[key] = new_idx
        return new_idx

    for _ in range(subdivisions):
        new_faces = []
        for face in faces:
            v1_idx, v2_idx, v3_idx = face
            
            a_idx = get_midpoint(v1_idx, v2_idx)
            b_idx = get_midpoint(v2_idx, v3_idx)
            c_idx = get_midpoint(v3_idx, v1_idx)
            
            new_faces.append((v1_idx, a_idx, c_idx))
            new_faces.append((v2_idx, b_idx, a_idx))
            new_faces.append((v3_idx, c_idx, b_idx))
            new_faces.append((a_idx, b_idx, c_idx))
        faces = new_faces

    #scale by radius
    vertices = [list(np.array(v) * radius) for v in vertices]
    return vertices, faces

sphere_vertices, sphere_faces = gen_sphere(radius=1.0, subdivisions=0)

write_stl(sphere_vertices, sphere_faces, "model.stl")
print(f"model.stl: {len(sphere_faces)} triangles")
write_raw(sphere_vertices, sphere_faces, "model.raw")
print(f"model.raw: {len(sphere_vertices)} vertices, {len(sphere_faces)} triangles")
