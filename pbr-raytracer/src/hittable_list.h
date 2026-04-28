#pragma once
#include "hittable.h"
#include <vector>
#include <memory>

// 여러 hittable 을 묶는 컨테이너
// 자기도 hittable 을 상속하므로, 씬 전체를 단 하나의 hittable 처럼 다룰 수 있다.
//
// shared_ptr 사용 이유
// - 동일 오브젝트를 여러 리스트가 공유할 수 있게 (재사용)
// - 수동 delete 없이 자동 메모리 관리
class hittable_list : public hittable
{
public:
    std::vector<std::shared_ptr<hittable>> objects;

    hittable_list() = default;
    hittable_list(std::shared_ptr<hittable> object) { add(object); }

    void clear() { objects.clear(); }
    void add(std::shared_ptr<hittable> object) { objects.push_back(object); }

    bool hit(const ray& r, interval ray_t, hit_record& rec) const override
    {
        hit_record temp_rec;
        bool hit_anything = false;
        double closest_so_far = ray_t.max;

        // 모든 오브젝트를 한 번씩 순회하며 가장 가까운 충돌을 갱신
        // 핵심 : 다음 호출의 t_max 를 closest_so_far 로 좁혀, 더 먼 충돌은 자동으로 무시
        for (const auto& object : objects)
        {
            if(object->hit(r, interval(ray_t.min, closest_so_far), temp_rec))
            {
                hit_anything = true;
                closest_so_far = temp_rec.t;
                rec = temp_rec;
            }
        }

        return hit_anything;
    }
};