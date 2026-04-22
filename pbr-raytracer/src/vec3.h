#pragma once
#include <cmath>
#include <iostream>

// 3차원 벡터 클래스
// 위치(point), 방향(direction), 색상(color) 모두 이 타입으로 표현한다.
// PBR에서 모든 빛 계산은 벡터 연산(내적, 외적, 정규화)으로 이루어진다.
class vec3
{
public:
    double e[3];

    vec3() : e{0, 0, 0} {}
    vec3(double e0, double e1, double e2) : e{e0, e1, e2} {}

    double x() const { return e[0]; }
    double y() const { return e[1]; }
    double z() const { return e[2]; }

    vec3 operator-() const { return vec3(-e[0], -e[1], -e[2]); }
    double operator[](int i) const { return e[i]; }
    double& operator[](int i) { return e[i]; }

    vec3& operator+=(const vec3& v)
    {
        e[0] += v.e[0];
        e[1] += v.e[1];
        e[2] += v.e[2];
        return *this;
    }

    vec3& operator*=(double t)
    {
        e[0] *= t;
        e[1] *= t;
        e[2] *= t;
        return *this;
    }

    vec3& operator/=(double t) { return *this *= 1 / t; }

    // 벡터의 길이 (크기)
    double length() const { return std::sqrt(length_squared()); }

    // 제곱 길이 — sqrt 연산이 비싸므로 비교할 때는 이걸 사용
    double length_squared() const
    {
        return e[0]*e[0] + e[1]*e[1] + e[2]*e[2];
    }
};

// vec3를 point3, color 용도로도 사용 (의미를 명확히 하기 위한 별칭)
using point3 = vec3;
using color  = vec3;

// =============================================================================
// vec3 유틸리티 함수
// =============================================================================

inline std::ostream& operator<<(std::ostream& out, const vec3& v)
{
    return out << v.e[0] << ' ' << v.e[1] << ' ' << v.e[2];
}

inline vec3 operator+(const vec3& u, const vec3& v)
{
    return vec3(u.e[0]+v.e[0], u.e[1]+v.e[1], u.e[2]+v.e[2]);
}

inline vec3 operator-(const vec3& u, const vec3& v)
{
    return vec3(u.e[0]-v.e[0], u.e[1]-v.e[1], u.e[2]-v.e[2]);
}

inline vec3 operator*(const vec3& u, const vec3& v)
{
    return vec3(u.e[0]*v.e[0], u.e[1]*v.e[1], u.e[2]*v.e[2]);
}

inline vec3 operator*(double t, const vec3& v)
{
    return vec3(t*v.e[0], t*v.e[1], t*v.e[2]);
}

inline vec3 operator*(const vec3& v, double t) { return t * v; }

inline vec3 operator/(const vec3& v, double t) { return (1/t) * v; }

// 내적 (dot product)
// 두 벡터가 얼마나 같은 방향을 향하는지를 나타낸다.
// 빛 계산에서 NdotL (법선·광원 방향) 등에 핵심적으로 사용된다.
// 결과: 같은 방향=양수, 수직=0, 반대 방향=음수
inline double dot(const vec3& u, const vec3& v)
{
    return u.e[0]*v.e[0] + u.e[1]*v.e[1] + u.e[2]*v.e[2];
}

// 외적 (cross product)
// 두 벡터에 모두 수직인 벡터를 구한다.
// 주로 좌표계(카메라 up/right 벡터)나 법선 계산에 사용된다.
inline vec3 cross(const vec3& u, const vec3& v)
{
    return vec3(
        u.e[1]*v.e[2] - u.e[2]*v.e[1],
        u.e[2]*v.e[0] - u.e[0]*v.e[2],
        u.e[0]*v.e[1] - u.e[1]*v.e[0]
    );
}

// 단위 벡터 (길이를 1로 정규화)
// 방향만 필요하고 크기는 필요 없을 때 사용한다.
// 광선의 방향 벡터, 법선 벡터는 항상 단위 벡터여야 한다.
inline vec3 unit_vector(const vec3& v) { return v / v.length(); }
