import numpy as np
from BoundingBox import BoundingBox


class FileReader:

    def __init__(self, filename):
        self.vbo_data = []
        self.sorted_Objectlines = {}
        self._faces_and_normals = []
        self.readFile(filename)
        self.parseFile()
        self.generate_vboData()

    def _put_line_in_list_from_dictionary(self, key, line):

        key = key.strip()

        if key not in self.sorted_Objectlines:
            self.sorted_Objectlines[key] = []

        line_split = line.split()
        line_split.pop(0)

        self.sorted_Objectlines[key].append(line_split)

    def readFile(self, filename):
        for line in open(filename, "r"):

            existing_keywords = [
                # '#',  # comments
                # 'mtllib',  # material library
                # 'o',  # object name
                'vn',  # vertex normals
                'v',  # geometric vertices
                # 'vt',  # texture vertices
                'f',  # face
                # 's',  # smoothing group
            ]

            [
                self._put_line_in_list_from_dictionary(keyword, line)
                for keyword in existing_keywords
                if line.startswith(keyword + ' ')
            ]

    def parseFile(self):
        vertices = []
        normals = []

        if 'v' in self.sorted_Objectlines:
            vertices = [
                list(map(float, vertex_line_split))
                for vertex_line_split in self.sorted_Objectlines['v']
            ]

        if 'vn' in self.sorted_Objectlines:
            normals = [
                list(map(float, vertex_normal_line_split))
                for vertex_normal_line_split in self.sorted_Objectlines['vn']
            ]

        bounding_box = BoundingBox(vertices)
        bounding_box.moveToCenter()
        bounding_box.scaleToBoundingBox()
        bounding_box.move_up()
        vertices = bounding_box.points

        if 'f' in self.sorted_Objectlines:
            for face_line_split in self.sorted_Objectlines['f']:
                points_indices = []
                normals_indices = []

                for value in face_line_split:
                    # case v//vn
                    if "//" in value:
                        data = value.split('//')

                        if len(data) > 0 and len(data[0]) > 0:
                            points_indices.append(int(data[0]) - 1)  # corrected vertex index
                        if len(data) > 1 and len(data[1]) > 0:
                            normals_indices.append(int(data[1]) - 1)  # corrected normal index

                    # case v/vt/vn undefined (we don't need textures yet)
                    # elif '/' in value:
                    #     print("case v/vt/vn")

                    # case v
                    elif len(value) > 0:
                        points_indices.append(int(value) - 1)  # corrected vertex index

                face = []
                points = []
                norms = []


                points.append(vertices[points_indices[0]])
                points.append(vertices[points_indices[1]])
                points.append(vertices[points_indices[2]])

                if len(normals_indices) == 0:
                    vector1 = np.array(points[2]) - np.array(points[0])
                    vector2 = np.array(points[2]) - np.array(points[1])

                    norm = np.cross(vector1, vector2)

                    norms.append(norm)
                    norms.append(norm)
                    norms.append(norm)

                else:
                    norms.append(normals[normals_indices[0]])
                    norms.append(normals[normals_indices[1]])
                    norms.append(normals[normals_indices[2]])

                #face = edge of a Triangle
                face.append(points)
                face.append(norms)
                #faces and normals = Triangle
                self._faces_and_normals.append(face)

    def generate_vboData(self):
        for face in self._faces_and_normals:
            vertices = face[0]
            norms = face[1]
            #vertices + normal for each edge of the Triangle
            for i in range(len(vertices)):
                self.vbo_data.append(np.concatenate((vertices[i], norms[i]), axis=None))
