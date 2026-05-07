#pragma once
#include "rtweekend.h"
#include "hittable.h"
#include "material.h"

// 카메라 + 렌더 루프를 한 클래스로 묶음
// main.cpp 는 Scene을 만들고 camera.render(world) 한 줄만 호출하면 됨
class camera
{
public:
    // 외부에서 조절하는 설정값
    double aspect_ratio = 1.0;  // 가로 / 세로 비율
    int image_width = 100;      // 가로 픽셀 수
    int samples_per_pixel = 10; // 픽셀상 샘플 수(안티엘리어싱용)
    int max_depth = 10;         // 광선이 최대 몇 번 반사될 수 있는가?

    double vfov = 90;                  // 수직 시야각 (degrees)
    point3 lookfrom = point3(0, 0, 0); // 카메라 위치
    point3 lookat = point3(0, 0, -1);  // 바라보는 지점
    vec3 vup = vec3(0, 1, 0);          // 카메라 위쪽 방향 (월드 업)

    // Scene과 출력 스트림을 받아 PPM 출력
    void render(const hittable &world, std::ostream &out)
    {
        initialize();

        out << "P3\n"
            << image_width << ' ' << image_height << "\n255\n";

        for (int j = 0; j < image_height; j++)
        {
            std::clog << "\rScanlines remaining: " << (image_height - j) << "  " << std::flush;
            for (int i = 0; i < image_width; i++)
            {
                // 픽셀 (i, j)에 대해 N개의 샘플을 누적한 뒤 평균
                color pixel_color(0, 0, 0);
                for (int s = 0; s < samples_per_pixel; s++)
                {
                    ray r = get_ray(i, j);                         // 픽셀 안 무작위 위치로 광선 1개 발사
                    pixel_color += ray_color(r, max_depth, world); // 그 광선의 색을 누적
                }
                write_color(out, pixel_samples_scale * pixel_color);
            }
        }
        std::clog << "\rDone.               \n";
    }

private:
    int image_height;           // 세로 픽셀 수 (계산됨)
    double pixel_samples_scale; // 1.0 / samples_per_pixel - 평균용 가중치
    point3 center;              // 카메라 위치
    point3 pixel00_loc;         // (0, 0) 픽셀의 중심 좌표
    vec3 pixel_delta_u;         // 가로 한 픽셀 이동량
    vec3 pixel_delta_v;         // 세로 한 픽셀 이동량
    vec3 u, v, w;               // 카메라 로컬 좌표축 (오른쪽, 위, 뒤)

    // 모든 내부 값을 한 번에 계산. render() 시작 시 호출됨.
    void initialize()
    {
        image_height = int(image_width / aspect_ratio);
        if (image_height < 1)
            image_height = 1;

        pixel_samples_scale = 1.0 / samples_per_pixel;

        center = lookfrom;

        // FOV -> 뷰포트 높이 변환
        // h = tan(vfov/2) : focal_length = 1 기준 뷰포트 절반 높이
        double focal_length = (lookfrom - lookat).length();
        double theta = degrees_to_radians(vfov);
        double h = std::tan(theta / 2);
        double viewport_height = 2.0 * h * focal_length;
        double viewport_width = viewport_height * (double(image_width) / image_height);

        // 카메라 로컬 좌표계 구성
        w = unit_vector(lookfrom - lookat); // 뒤쪽 (바라보는 방향의 반대)
        u = unit_vector(cross(vup, w));     // 오른쪽 (vup × w)
        v = cross(w, u);                    // 위쪽 (w × u, 자동 결정)

        // 뷰포트 벡터를 세계 x/y 축 대신 카메라 로컬 u/v 축으로 구성
        vec3 viewport_u = viewport_width * u;   // 뷰포트 가로 방향
        vec3 viewport_v = -viewport_height * v; // 뷰포트 세로 방향 (아래가 양의 j이므로 -v)

        pixel_delta_u = viewport_u / image_width;
        pixel_delta_v = viewport_v / image_height;

        // 뷰포트 왼쪽 위 모서리 : 카메라에서 앞으로(-w) focal_length만큼, 뷰포트 절반씩 이동
        point3 viewport_upper_left = center - (focal_length * w) - viewport_u / 2 - viewport_v / 2;
        pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v);
    }

    // 픽셀 (i, j) 안의 무작위 위치를 향해 광선 1개를 만든다.
    ray get_ray(int i, int j) const
    {
        vec3 offset = sample_square(); // [-0.5, +0.5)² 안의 점 = 픽셀 안 무작위 지점
        point3 pixel_sample = pixel00_loc + ((i + offset.x()) * pixel_delta_u) + ((j + offset.y()) * pixel_delta_v);
        vec3 ray_direction = pixel_sample - center;
        return ray(center, ray_direction);
    }

    // 단위 사각형 [-0.5, +0.5)² 안의 무작위 점 (z=0)
    // 픽셀 중심을 (0, 0)으로 두고 그 주변에 균등 분포로 흩뿌린다.
    vec3 sample_square() const
    {
        return vec3(random_double() - 0.5, random_double() - 0.5, 0);
    }

    // 광선이 Scene과 교차하면 법선으로 색으로, 아니면 하늘 그라디언트
    color ray_color(const ray &r, int depth, const hittable &world) const
    {
        // 최대 반사 횟수 초과 -> 더 이상 빛을 추적하지 않음, 검정 반환
        if (depth <= 0)
            return color(0, 0, 0);

        hit_record rec;
        // t_min = 0.001 : 부동소수점 오차로 자기 자신을 다시 때리는 현상(shadow acne) 방지
        if (world.hit(r, interval(0.001, infinity), rec))
        {
            ray scattered;
            color attenuation;

            // 재질에게 "이 광선이 어디로 튀는가?"를 묻는다.
            if (rec.mat->scatter(r, rec, attenuation, scattered))
                return attenuation * ray_color(scattered, depth - 1, world);

            // scatter가 false면 빛이 흡수됨 -> 검정
            return color(0, 0, 0);
        }

        vec3 unit_dir = unit_vector(r.direction());
        double a = 0.5 * (unit_dir.y() + 1.0);
        return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0);
    }
};