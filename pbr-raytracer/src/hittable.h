#pragma once
#include "vec3.h"
#include "ray.h"
#include "interval.h"

// 광선이 어떤 표면에 부딪혔을 때, 그 충돌에 대한 정보를 한 묶음으로 담는다.
// - p : 충돌 지점의 3D 좌표
// - normal : 표면 법선 (단위벡터, 항상 광선의 반대 방향을 향함)
// - t : 광선 방정식 P(t) = A + tb 의 t값
// - front_face : 광선이 표면을 앞에서 맞았는가?
struct hit_record
{
	point3 p;
	vec3 normal;
	double t;
	bool front_face;

	// 외향 법선 (밖을 향하는 단위벡터)를 받아, 광선과의 부호로 앞/뒷면 판별
	// - 광선과 외향 법선이 반대 방향 (내적 < 0) -> 광선이 밖에서 들어옴 -> 앞면
	// - 광선과 외향 법선이 같은 방향 (내적 > 0) -> 광선이 안에서 나감 -> 뒷면, 법선 뒤집음
	void set_face_normal(const ray& r, const vec3& outward_normal)
	{
		front_face = dot(r.direction(), outward_normal) < 0.0;
		normal = front_face ? outward_normal : -outward_normal;
	}
};

// "광선에 맞을 수 있는 모든 것"의 추상 인터페이스
// 구, 평면, 삼각형, 메시 등은 모두 이 클래스를 상속해서 hit() 을 구현한다.
class hittable
{
public:
	virtual ~hittable() = default;

	// 광선 r이 t범위 ray_t 안에서 이 오브젝트와 교차하는지 검사
	// 교차하면 rec 에 충돌 정보를 채우고 true 반환, 아니면 false
	virtual bool hit(const ray& r, interval ray_t, hit_record& rec) const = 0;
};