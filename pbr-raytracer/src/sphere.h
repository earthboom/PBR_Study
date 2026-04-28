#pragma once
#include "hittable.h"
#include "vec3.h"

class sphere : public hittable
{
public:
    sphere(const point3& center, double radius)
        : center(center), radius(std::fmax(0.0, radius)) {}
    
    bool hit(const ray& r, interval ray_t, hit_record& rec) const override
    {
        // Ch4. 에서 유도한 이차방정식 풀이를 그대로 옮김
        vec3 oc = center - r.origin();
        double a = r.direction().length_squared();
        double h = dot(r.direction(), oc);
        double c = oc.length_squared() - radius * radius;

        double discriminant = h * h - a * c;
        if(discriminant < 0)
            return false;
        
        double sqrtd = std::sqrt(discriminant);

        // 두 근 중 ray_t 범위 안에 들어오는 가까운 쪽을 먼저 시도
        double root = (h - sqrtd) / a;
        if(!ray_t.surrounds(root))
        {
            root = (h + sqrtd) / a;
            if(!ray_t.surrounds(root))
                return false;
        }

        // 충돌 정보 채우기
        rec.t = root;
        rec.p = r.at(root);
        vec3 outward_normal = (rec.p - center) / radius;    // 단위 벡터 (P-C 길이는 항상 radius)
        rec.set_face_normal(r, outward_normal);

        return true;
    }

private:
    point3 center;
    double radius;
};