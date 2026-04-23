#pragma once
#include "vec3.h"

// 광선(Ray) 클래스
// 레이트레이서의 핵심 개념: 광선 = 출발점 + 방향 * t
// P(t) = origin + t * direction
//
// t 값에 따라:
//   t = 0  → 출발점(origin) 자체
//   t > 0  → 광선이 향하는 방향 (앞쪽)
//   t < 0  → 광선 반대 방향 (뒤쪽, 일반적으로 무시)
class ray
{
public:
    ray() {}
    ray(const point3& origin, const vec3& direction)
        : orig(origin), dir(direction) {}

    const point3& origin()    const { return orig; }
    const vec3&   direction() const { return dir; }

    // t 값에 해당하는 광선 위의 점을 반환
    point3 at(double t) const { return orig + t * dir; }

private:
    point3 orig;
    vec3   dir;
};
