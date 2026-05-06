#pragma once
#include "rtweekend.h"
#include "ray.h"
#include "color.h"

/**
 * @brief 구조 설명
 * material - scatter(광선이 어디로 튀는가?)를 정의하는 추상 인터페이스
 * lambertian - 기존 확산 재질. 법선 기준 반구 위 무작위 방향으로 scatter
 * metal - 반사 방향으로 scatter. fuzz로 약간의 흐림 추가
 */

// hit_record 전방 선언 (material <-> hit_record가 서로를 참조하므로)
struct hit_record;

// "표면 재밀"의 인터페이스
// scatter() :  입사 광선을 받아 산란 광선과 감쇠 색을 돌려줌
//              반환값 false = 빛이 완전 흡수됨 (더 이상 추적 불필요)
class material
{
public:
    virtual ~material() = default;

    virtual bool scatter(const ray &r_in, const hit_record &rec, color &attenuation, ray &scattered) const = 0;
};

// 람베르트 확산 재질 - 빛을 법선 방향 반구 위 무작위 방향으로 산란
class lambertian : public material
{
public:
    lambertian(const color &albedo) : albedo(albedo) {}

    bool scatter(const ray &r_in, const hit_record &rec, color &attenuation, ray &scattered) const override
    {
        // 법선 + 단위구 표면 위 무작위 벡터 = 람베르트 코사인 분포
        vec3 scatter_direction = rec.normal + random_unit_vector();

        // 산란 방향이 거의 0에 가까우면(법선과 정반대로 뽑힌 경우) 법선으로 대체
        // 이 처리 없으면 무한대/NaN 광선이 생긴다.
        if (scatter_direction.near_zero())
            scatter_direction = rec.normal;

        scattered = ray(rec.p, scatter_direction);
        attenuation = albedo;
        return true;
    }

private:
    color albedo; // 표면 반사율 (0 = 완전 흡수, 1 = 완전 반사)
};

// 금속 재질 - 입사 광선을 법선에 대해 반사
class metal : public material
{
public:
    // fuzz : 반사 방향에 추가하는 무작위 흐림 (0=완벽한 거울, 1=매우 흐림)
    metal(const color &albedo, double fuzz)
        : albedo(albedo), fuzz(fuzz < 1 ? fuzz : 1) {}

    bool scatter(const ray &r_in, const hit_record &rec, color &attenuation, ray &scattered) const override
    {
        // 정반사 방향 계산 : v - 2(v * n) * n
        vec3 reflected = reflect(r_in.direction(), rec.normal);

        // fuzz : 반사 방향을 단위구 표면 위 무작위 벡터만큼 흔들어줌
        reflected = unit_vector(reflected) + (fuzz * random_unit_vector());
        scattered = ray(rec.p, reflected);
        attenuation = albedo;

        // 반사 방향이 표면 안쪽을 향하면(fuzz가 너무 크면) 빛 흡수 처리
        return dot(scattered.direction(), rec.normal) > 0;
    }

private:
    color albedo;
    double fuzz;
};