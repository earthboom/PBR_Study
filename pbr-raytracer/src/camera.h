#pragma once
#include "rtweekend.h"
#include "hittable.h"

// 카메라 + 렌더 루프를 한 클래스로 묶음
// main.cpp 는 Scene을 만들고 camera.render(world) 한 줄만 호출하면 됨
class camera
{
public:
    // 외부에서 조절하는 설정값
    double aspect_ratio = 1.0;  // 가로 / 세로 비율
    int image_width = 100;      // 가로 픽셀 수
    int samples_per_pixel = 10; // 픽셀상 샘플 수(안티엘리어싱용)

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
                    ray r = get_ray(i, j);
                    pixel_color += ray_color(r, world);
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
    point3 pixel00_loc;        // (0, 0) 픽셀의 중심 좌표
    vec3 pixel_delta_u;         // 가로 한 픽셀 이동량
    vec3 pixel_delta_v;         // 세로 한 픽셀 이동량

    // 모든 내부 값을 한 번에 계산. render() 시작 시 호출됨.
    void initialize()
    {
        image_height = int(image_width / aspect_ratio);
        if (image_height < 1)
            image_height = 1;

        pixel_samples_scale = 1.0 / samples_per_pixel;

        center = point3(0, 0, 0);

        // viewport
        double focal_length = 1.0;
        double viewport_height = 2.0;
        double viewport_width = viewport_height * (double(image_width) / image_height);

        vec3 viewport_u(viewport_width, 0, 0);
        vec3 viewport_v(0, -viewport_height, 0);

        pixel_delta_u = viewport_u / image_width;
        pixel_delta_v = viewport_v / image_height;

        point3 viewport_upper_left = center - vec3(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2;
        pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v);
    }

    // 픽셀 (i, j) 안의 무작위 위치를 향해 광선 1개를 만든다.
    ray get_ray(int i, int j) const
    {
        vec3 offset = sample_square(); // [-0.5, +0.5)² 안의 점
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
    color ray_color(const ray &r, const hittable &world) const
    {
        hit_record rec;
        if (world.hit(r, interval(0.0, infinity), rec))
            return 0.5 * (rec.normal + color(1, 1, 1));

        vec3 unit_dir = unit_vector(r.direction());
        double a = 0.5 * (unit_dir.y() + 1.0);
        return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0);
    }
};