# coding: UTF-8
import sys
import re

args = sys.argv
argc = len(args)

SHADER_FILE = 'shader.txt'

OUT_SHADER_FILE = 'ConvertedGLSLShader'
if argc >= 2:
	OUT_SHADER_FILE = args[1]

DELETABLE_CODES = ["#ifdef GL_ES","precision mediump float;","precision highp float;","#endif","#extension GL_OES_standard_derivatives : enable","#extension GL_OES_standard_derivatives : disable","uniform"]

glslToHLSL = {'gl_FragCoord':'(i.uv*_ScreenParams)','resolution':'_ScreenParams',
'vec2':'float2', 'vec3':'float3', 'vec4':'float4', 
'mat2':'float2x2', 'mat3':'float3x3', 'mat4':'float4x4',
'time':'_Time.y','mouse':'float2(0.5,0.5)','fract':'frac','mix':'lerp','atan':'atan2','texture2D':'tex2D','point':'hlslPoint'}

codeBegin = 'Shader "'+OUT_SHADER_FILE+'"\n' \
    '{\n' \
    'SubShader\n' \
    '{\n' \
    'Pass\n' \
    '{\n' \
    '\tCGPROGRAM\n' \
    '\t#pragma vertex vert_img\n' \
    '\t#pragma fragment frag\n' \
    '\t#include "UnityCG.cginc"\n'

codeModFunc = '\tfloat mod(float a, float b) {\n' \
    '\t\treturn a - floor(a / b) * b;\n' \
    '\t}\n'

codeEnd = 'ENDCG\n' \
	'\t\t}\n' \
	'\t}\n' \
	'}\n'

def checkHasDeletableCodes(str):
	for i in range(len(DELETABLE_CODES)):
		if re.compile(DELETABLE_CODES[i]).search(str):
			#print 'deleteKeyWords ->',DELETE_KEY_WORDS[i]
			return True
	return False

def replaceMainCode(str):
	main = ""
	if re.compile('void main').search(str):
		main = str.replace(' ',"")
		main = main.replace('voidmain(void)',"fixed4 frag (v2f_img i) : SV_Target")
		main = main.replace('voidmain()',"fixed4 frag (v2f_img i) : SV_Target")
		return main
	return str

def replaceFragColorCode(str):
	frag = "" 
	if re.compile('gl_FragColor').search(str):
		frag = str.replace(' ',"")
		rep = 'gl_FragColor='
		if re.compile(rep).search(frag):
			frag = frag.replace('gl_FragColor=',"return ")
		else:
			frag = str
		return frag
	return str

def replaceGLSLToHLSLCode(str):
	res = str
	for key, value in glslToHLSL.iteritems():
		#res = res.replace(key,value)
		pattern = key
		matches = re.finditer(pattern, str)
		for match in matches:
			m = match.group()
			res = res.replace(key,value)
		#print "key:", key, "-- value:", value 
	return res

#Replace vec3(1) shortcut constructors in which all elements have same value with explicit float3(1,1,1)
def replaceVector(l):
	vcoce = l
	for i in range(2,5):
		pattern = r'vec'+str(i)+'\([\sa-zA-Z0-9.]+\)'
		matches = re.finditer(pattern, vcoce)
		for match in matches:
			vec = 'vec'+str(i)
			m = match.group()
			val = m.replace(vec+'(',"")
			val = val.replace(')',"")

			res = vec+'('
			for j in range(i):
				if j == i-1:
					res += val
				else:
					res += val+','
			res += ')'

			vcoce = vcoce.replace(m,res)
			#print vcoce

	# replace "vec4(finalColor,1.0)" this kind of format
	pattern = r'vec4\([\sa-zA-Z0-9._]+'','+ r'[\s0-9.]+\)'
	matches = re.finditer(pattern, vcoce)
	for match in matches:
		m = match.group()
		vals = m.split(",")
		val = vals[0].replace('','')
		val = val.replace('vec4(','')
		val = 'vec4('+val+'.x, '+val+'.y, '+val+'.z, '+vals[1]
		vcoce = vcoce.replace(m,val)
		#print val
	return vcoce


def outShaderFile():
	code = ''

	f = open(SHADER_FILE)
	data = f.read()
	f.close()

	lines = data.split('\n')
	for line in lines:
		line = replaceMainCode(line)
		line = replaceFragColorCode(line)
		line = replaceVector(line)
		line = replaceGLSLToHLSLCode(line)

		hasDeletableCode = checkHasDeletableCodes(line)
		if hasDeletableCode != True:
			code += '\t'+line+'\n'
	   	#print line

	finalCode = ''
	if re.compile('mod').search(data):
		finalCode = codeBegin+codeModFunc+code+codeEnd
	else:
		finalCode = codeBegin+code+codeEnd
	#print finalCode

	f = open(OUT_SHADER_FILE+'.shader', 'w')
	f.write(finalCode)
	f.close()

outShaderFile()




