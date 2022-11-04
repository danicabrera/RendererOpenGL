vertex_shader ='''
#version 450 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texcoords;
layout (location = 2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float time;


out vec2 UVs;
out vec3 norms;
out vec3 pos;

void main()
{
    
   
    UVs = texcoords;
    norms = normals;
    pos = (modelMatrix * vec4(position, 1.0)).xyz;
    
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
    
     
}
'''

fragment_shader ='''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform vec3 pointLight;
uniform sampler2D tex;


void main()
{
    float intensity = dot(norms, normalize(pointLight - pos));
    fragColor = texture(tex, UVs) * intensity;
}
'''

fragment_toon_shader ='''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform vec3 pointLight;
uniform sampler2D tex;


void main()
{
    float intensity = dot(norms, normalize(pointLight - pos));
    if(intensity < 0.2){
        intensity = 0.1;
    }
    else if (intensity < 0.5){
        intensity = 0.4;
    }
    else if (intensity < 0.8){
        intensity = 0.7;
    }
        

    
    fragColor = texture(tex, UVs) * intensity;
}
'''



fragment_glow = '''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform vec3 pointLight;
uniform mat4 color;
uniform sampler2D tex;


void main()
{
    float intensity = dot(norms, normalize(pointLight - pos));
    
    vec3 color = vec3(1,1,0);
    vec3 dir = vec3(0,1,0); // high noon  
    vec4 returnColor = vec4(color, 1.0);
    vec3 fNormal = vec3(1,0,1);
    float diffuse = .25 + dot(fNormal,dir);
    
    fragColor = (texture(tex, UVs) * intensity) + (returnColor*diffuse);
    
    
}
'''

fragment_colors = '''
#version 450 core

out vec4 fragColor;

in vec2 UVs;
in vec3 norms;
in vec3 pos;

uniform vec3 pointLight;
uniform mat4 color;
uniform sampler2D tex;


void main()
{
    float intensity = dot(norms, normalize(pointLight - pos));

    vec3 color = vec3(pos* 0.5 + 0.5);
    vec3 dir = vec3(0,1,0); // high noon  
    vec4 returnColor = vec4(color, 1.0);
    vec3 fNormal = vec3(-1,0,-1);
    float diffuse = .25 + dot(fNormal,dir);

    fragColor = (texture(tex, UVs) * intensity) + (returnColor*diffuse);


}
'''