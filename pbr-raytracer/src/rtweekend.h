#pragma once
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <memory>

// 자주 쓰는 표준 라이브러리 심볼을 가져온다 (using 으로 짧게).
using std::shared_ptr;
using std::make_shared;

// 자주 쓰는 상수
constexpr double infinity = std::numeric_limits<double>::infinity();
constexpr double pi       = 3.1415926535897932385;

// 각도 ↔ 라디안 변환
inline double degrees_to_radians(double degrees) { return degrees * pi / 180.0; }

// [0, 1) 범위의 균등분포 무작위 실수.
// std::rand() 는 [0, RAND_MAX] 정수를 돌려주므로 (RAND_MAX + 1.0) 으로 나누면
// 결과가 [0, 1) 이 되어 1.0을 절대 포함하지 않는다.
inline double random_double()
{
    return std::rand() / (RAND_MAX + 1.0);
}

// [min, max) 범위의 균등분포 무작위 실수.
inline double random_double(double min, double max)
{
    return min + (max - min) * random_double();
}

// 프로젝트 공통 헤더들 (이 헤더 하나만 include 하면 끝)
#include "vec3.h"
#include "ray.h"
#include "interval.h"
#include "color.h"
