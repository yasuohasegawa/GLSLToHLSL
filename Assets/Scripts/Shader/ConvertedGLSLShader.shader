Shader "ConvertedGLSLShader"
{
SubShader
{
Pass
{
	CGPROGRAM
	#pragma vertex vert_img
	#pragma fragment frag
	#include "UnityCG.cginc"
	float mod(float a, float b) {
		return a - floor(a / b) * b;
	}
	
	
	
	fixed4 frag (v2f_img i) : SV_Target{
	
		float2 uv = ( (i.uv*_ScreenParams).xy / _ScreenParams.x) - 0.25;	
		
		uv.y = abs(uv.y);
		
		uv.y += 0.005 * (1.0 + cos(_Time.y * 3.2));
		uv.y = max(float2(0.5,0.5).x * 0.2, uv.y);
		uv.x /= uv.y;
		
		
		uv.x += _Time.y;
		
		
		float color = mod(floor(uv.x) + floor(uv.y * 2.0), 2.0) + 0.5;
		float dist = sqrt(uv.y) * 1.0;
		color = color * max(0.1, min(1.0, dist * 1.3));
		
		return float4(color,color,color,color);
	
	}
ENDCG
		}
	}
}
