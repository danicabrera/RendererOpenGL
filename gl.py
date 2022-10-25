import glm #pip install PyGLM

from numpy import array, float32

# pip install PyOpenGL
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class Buffer(object):
    def __init__(self, data):
        self.data = data

        self.createVertexBuffer()

        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)

    def createVertexBuffer(self):
        self.vertBuffer = array(self.data, dtype = float32)

        # Vertex Buffer Object
        self.VBO = glGenBuffers(1)

        # Vertex Array Object
        self.VAO = glGenVertexArrays(1)

    def render(self):

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindVertexArray(self.VAO)

        # Mandar la informacion de vertices
        glBufferData(GL_ARRAY_BUFFER,           # Buffer ID
                     self.vertBuffer.nbytes,    # Buffer size in bytes
                     self.vertBuffer,           # Buffer data
                     GL_STATIC_DRAW)            # Usage

        # Atributos

        # Atributo de posiciones
        glVertexAttribPointer(0,                # Attribute number
                              3,                # Size
                              GL_FLOAT,         # Type
                              GL_FALSE,         # Is it normalized
                              4 * 6,            # Stride
                              ctypes.c_void_p(0))# Offset

        glEnableVertexAttribArray(0)

        # Atributo de color
        glVertexAttribPointer(1,                # Attribute number
                              3,                # Size
                              GL_FLOAT,         # Type
                              GL_FALSE,         # Is it normalized
                              4 * 6,            # Stride
                              ctypes.c_void_p(4*3))# Offset

        glEnableVertexAttribArray(1)

        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertBuffer) / 6) )


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0,0, self.width, self.height)

        self.scene = []
        self.active_shader = None

        #ViewMatrix
        self.camPosition = glm.vec3(0,0,0)
        self.camRotation = glm.vec3(0,0,0)

        self.ViewMatrix = self.getViewMatrix()

        self.projectionMatrix = glm.perspective(glm.radians(60),            #FOV
                                                self.width / self.height,   #Aspect Ratio
                                                0.1,                        #Near Plane
                                                1000                        #Far Plane
                                                )

    def getViewMatrix(self):
        identidad = glm.mat4(1)
        transalateMat = glm.translate(identidad, self.camPosition)

        pitch = glm.rotate(identidad, glm.radians(self.camRotation.x), glm.vec3(1,0,0))
        yaw = glm.rotate(identidad, glm.radians(self.camRotation.x), glm.vec3(0, 1, 0))
        roll = glm.rotate(identidad, glm.radians(self.camRotation.x), glm.vec3(0, 0, 1))

        rotationMat = pitch * yaw * roll

        camMatrix = transalateMat * rotationMat

        return glm.inverse(camMatrix)

    def getModelMatrix(self):
        identidad = glm.mat4(1)
        transalateMat = glm.translate(identidad, self.camPosition)

        pitch = glm.rotate(identidad, glm.radians(self.camRotation.x), glm.vec3(1,0,0))
        yaw = glm.rotate(identidad, glm.radians(self.camRotation.x), glm.vec3(0, 1, 0))
        roll = glm.rotate(identidad, glm.radians(self.camRotation.x), glm.vec3(0, 0, 1))

        rotationMat = pitch * yaw * roll

        scaleMat = glm.scale(identidad, transalateMat)

        return glm.inverse(scaleMat)



    def setShaders(self, vertexShader, fragmentShader):
        if vertexShader is not None and fragmentShader is not None:
            self.active_shader = compileProgram( compileShader(vertexShader, GL_VERTEX_SHADER),
                                                 compileShader(fragmentShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None

    def update(self):
        self.viewMatrix = self.getViewMatrix()

    def render(self):
        glClearColor(0.2,0.2,0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.active_shader is not None:
            glUseProgram(self.active_shader)

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "viewMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.viewMatrix))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projectionMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.projectionMatrix))

        for obj in self.scene:

            if self.active_shader is not None:
                glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "modelMatrix"),
                                   1, GL_FALSE, glm.value_ptr(obj.getModelMatrix()))

            obj.render()
