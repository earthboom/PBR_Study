#pragma once
#include "vec3.h"
#include "interval.h"
#include <iostream>

// 0~1 범위의 color 를 0~255 정수 RGB 로 변환해 PPM 스트림에 출력.
// 안티에일리어싱으로 평균낸 결과가 미세하게 1.0을 넘는 경우가 생기므로,
// 안전하게 [0, 0.999] 로 클램핑한 뒤 255.999를 곱한다.
inline void write_color(std::ostream& out, const color& pixel_color)
{
    static const interval intensity(0.000, 0.999);

    int ir = int(256 * intensity.clamp(pixel_color.x()));
    int ig = int(256 * intensity.clamp(pixel_color.y()));
    int ib = int(256 * intensity.clamp(pixel_color.z()));

    out << ir << ' ' << ig << ' ' << ib << '\n';
}
