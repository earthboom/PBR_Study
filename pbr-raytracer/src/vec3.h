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
    double &operator[](int i) { return e[i]; }

    vec3 &operator+=(const vec3 &v)
    {
        e[0] += v.e[0];
        e[1] += v.e[1];
        e[2] += v.e[2];
        return *this;
    }

    vec3 &operator*=(double t)
    {
        e[0] *= t;
        e[1] *= t;
        e[2] *= t;
        return *this;
    }

    vec3 &operator/=(double t) { return *this *= 1 / t; }

    // 벡터의 길이 (크기)
    double length() const { return std::sqrt(length_squared()); }

    // 제곱 길이 — sqrt 연산이 비싸므로 비교할 때는 이걸 사용
    double length_squared() const
    {
        return e[0] * e[0] + e[1] * e[1] + e[2] * e[2];
    }

    // 각 성분이 거의 0인치 확인 - 산란 방향이 영벡터가 되는 것을 방지
    bool near_zero() const
    {
        const double s = 1e-8;
        return (std::fabs(e[0]) < s) && (std::fabs(e[1]) < s) && (std::fabs(e[2]) < s);
    }

    // 각 성분이 [0, 1) 범위인 무작위 벡터
    static vec3 random()
    {
        return vec3(random_double(), random_double(), random_double());
    }

    // 각 성분이 [min, max) 범위인 무작위 벡터
    static vec3 random(double min, double max)
    {
        return vec3(random_double(min, max), random_double(min, max), random_double(min, max));
    }
};

// vec3를 point3, color 용도로도 사용 (의미를 명확히 하기 위한 별칭)
using point3 = vec3;
using color = vec3;

// =============================================================================
// vec3 유틸리티 함수
// =============================================================================

inline std::ostream &operator<<(std::ostream &out, const vec3 &v)
{
    return out << v.e[0] << ' ' << v.e[1] << ' ' << v.e[2];
}

inline vec3 operator+(const vec3 &u, const vec3 &v)
{
    return vec3(u.e[0] + v.e[0], u.e[1] + v.e[1], u.e[2] + v.e[2]);
}

inline vec3 operator-(const vec3 &u, const vec3 &v)
{
    return vec3(u.e[0] - v.e[0], u.e[1] - v.e[1], u.e[2] - v.e[2]);
}

inline vec3 operator*(const vec3 &u, const vec3 &v)
{
    return vec3(u.e[0] * v.e[0], u.e[1] * v.e[1], u.e[2] * v.e[2]);
}

inline vec3 operator*(double t, const vec3 &v)
{
    return vec3(t * v.e[0], t * v.e[1], t * v.e[2]);
}

inline vec3 operator*(const vec3 &v, double t) { return t * v; }

inline vec3 operator/(const vec3 &v, double t) { return (1 / t) * v; }

// 내적 (dot product)
// 두 벡터가 얼마나 같은 방향을 향하는지를 나타낸다.
// 빛 계산에서 NdotL (법선·광원 방향) 등에 핵심적으로 사용된다.
// 결과: 같은 방향=양수, 수직=0, 반대 방향=음수
inline double dot(const vec3 &u, const vec3 &v)
{
    return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] * v.e[2];
}

// 외적 (cross product)
// 두 벡터에 모두 수직인 벡터를 구한다.
// 주로 좌표계(카메라 up/right 벡터)나 법선 계산에 사용된다.
inline vec3 cross(const vec3 &u, const vec3 &v)
{
    return vec3(
        u.e[1] * v.e[2] - u.e[2] * v.e[1],
        u.e[2] * v.e[0] - u.e[0] * v.e[2],
        u.e[0] * v.e[1] - u.e[1] * v.e[0]);
}

// 단위 벡터 (길이를 1로 정규화)
// 방향만 필요하고 크기는 필요 없을 때 사용한다.
// 광선의 방향 벡터, 법선 벡터는 항상 단위 벡터여야 한다.
inline vec3 unit_vector(const vec3 &v) { return v / v.length(); }

// 단위구(반지름 1) 안의 무작위 점 - 기각 샘플링
// 전략: [-1, 1]³ 정육면체 안 점을 뽑고, 구 밖이면 버리고 다시 뽑는다.
// p.length_squared() < 1 이면 구 안에 있다는 뜻
inline vec3 random_in_unit_sphere()
{
    while (true)
    {
        vec3 p = vec3::random(-1, 1);
        if (p.length_squared() < 1)
            return p;
    }
}

// 단위구 표면 위의 무작위 점 (길이가 정확히 1인 방향벡터)
// random_in_unit_sphere()로 구 안의 점을 뽑은 뒤 정규화해서 표면으로 밀어낸다.
inline vec3 random_unit_vector()
{
    return unit_vector(random_in_unit_sphere());
}

// 법선 방향과 같은 반구 위의 무작위 단위벡터
// dot > 0 이면 법선과 같은 방향 (표면 바깥쪽) -> 그대로 사용
// dot < 0 이면 표면 안쪽을 향함 -> 뒤집는다
inline vec3 random_on_hemisphere(const vec3 &normal)
{
    vec3 on_unit_sphere = random_unit_vector();
    if (dot(on_unit_sphere, normal) > 0.0)
        return on_unit_sphere;
    else
        return -on_unit_sphere;
}

// 입시 벡터 v를 법선 n에 대해 반사 : v - 2(v * n) * n
inline vec3 reflect(const vec3 &v, const vec3 &n)
{
    return v - 2 * dot(v, n) * n;
}

inline vec3 refract(const vec3 &uv, const vec3 &n, double etai_over_etat)
{
    // cos ϴ : 입사 광선(뒤집어서)과 법선의 내적 - 입사각 코사인
    double cos_theta = fmin(dot(-uv, n), 1.0);
    vec3 r_out_perp = etai_over_etat * (uv + cos_theta * n);                            // 수직 성분
    vec3 r_out_parallel = -std::sqrt(std::fabs(1.0 - r_out_perp.length_squared())) * n; // 평행 성분
    return r_out_perp + r_out_parallel;
}