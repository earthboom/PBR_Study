#pragma once
#include <cmath>
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

// 프로젝트 공통 헤더들 (이 헤더 하나만 include 하면 끝)
#include "vec3.h"
#include "ray.h"
#include "interval.h"
