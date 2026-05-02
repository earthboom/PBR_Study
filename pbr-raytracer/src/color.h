#pragma once
#include "vec3.h"
#include "interval.h"
#include <iostream>

// 선형 색값 -> 감마 2 보정값 (sqrt)
// 모니터는 밝기를 선형으로 처리하지 않아, 어두운 값이 실제보다 훨씬 어둡게 보인다.
// sqrt를 취하면 어두운 영역이 밝아져 눈에 자연스럽게 보임
inline double linear_to_gamma(double linear_component)
{
    if (linear_component > 0)
        return std::sqrt(linear_component);
    return 0;
}

// 0~1 범위의 color 를 0~255 정수 RGB 로 변환해 PPM 스트림에 출력.
// 안티에일리어싱으로 평균낸 결과가 미세하게 1.0을 넘는 경우가 생기므로,
// 안전하게 [0, 0.999] 로 클램핑한 뒤 255.999를 곱한다.
inline void write_color(std::ostream &out, const color &pixel_color)
{
    // 감마 보정 먼저 적용한 뒤 클램핑
    double r = linear_to_gamma(pixel_color.x());
    double g = linear_to_gamma(pixel_color.y());
    double b = linear_to_gamma(pixel_color.z());

    static const interval intensity(0.000, 0.999);

    int ir = int(256 * intensity.clamp(r));
    int ig = int(256 * intensity.clamp(g));
    int ib = int(256 * intensity.clamp(b));

    out << ir << ' ' << ig << ' ' << ib << '\n';
}
