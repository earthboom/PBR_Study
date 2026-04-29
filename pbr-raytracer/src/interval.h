#pragma once
#include <limits>

// [min, max] 형태의 실수 구간을 한 변수로 다루는 작은 유틸.
// 광선의 t 허용 범위를 함수 사이에 깔끔히 전달하기 위해 사용한다.
class interval
{
public:
    double min, max;

    // 기본값: 빈 구간 (어떤 값도 포함하지 않음)
    interval() : min(+std::numeric_limits<double>::infinity()),
                 max(-std::numeric_limits<double>::infinity()) {}

    interval(double mn, double mx) : min(mn), max(mx) {}

    double size() const { return max - min; }

    // 경계 포함 (closed interval): min <= x <= max
    bool contains(double x) const { return min <= x && x <= max; }

    // 경계 제외 (open interval): min < x < max
    // 광선 충돌에서 자기 자신과의 충돌(t=0)을 배제할 때 주로 사용.
    bool surrounds(double x) const { return min < x && x < max; }

    // x 를 [min, max] 안으로 잘라낸다 (clamping).
    // 색상값을 [0, 1] 범위로 강제할 때 사용.
    double clamp(double x) const
    {
        if (x < min) return min;
        if (x > max) return max;
        return x;
    }

    // 자주 쓰는 미리 정의된 구간들
    static const interval empty;
    static const interval universe;
};

inline const interval interval::empty    = interval(+std::numeric_limits<double>::infinity(),
                                                    -std::numeric_limits<double>::infinity());
inline const interval interval::universe = interval(-std::numeric_limits<double>::infinity(),
                                                    +std::numeric_limits<double>::infinity());
