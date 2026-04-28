#include <iostream>
#include <fstream>
#include <filesystem>

#include "rtweekend.h"
#include "hittable.h"
#include "hittable_list.h"
#include "sphere.h"

void write_color(std::ostream& out, const color& pixel_color)
{
    int ir = int(255.999 * pixel_color.x());
    int ig = int(255.999 * pixel_color.y());
    int ib = int(255.999 * pixel_color.z());
    out << ir << ' ' << ig << ' ' << ib << '\n';
}

// 광선이 씬(world)과 교차하면 법선을 색상으로, 아니면 하늘 그라디언트를 반환.
// 이제 ray_color 는 오브젝트 종류를 전혀 모른다 — world.hit() 한 줄이면 끝.
color ray_color(const ray& r, const hittable& world)
{
    hit_record rec;
    if (world.hit(r, interval(0.0, infinity), rec))
    {
        // 법선(-1~+1)을 색상(0~1)으로 매핑
        return 0.5 * (rec.normal + color(1, 1, 1));
    }

    // 배경 — 하늘 그라디언트
    vec3 unit_dir = unit_vector(r.direction());
    double a = 0.5 * (unit_dir.y() + 1.0);
    return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0);
}

int main()
{
    // ── 이미지 설정 ──────────────────────────────────────────────
    double aspect_ratio = 16.0 / 9.0;
    int    image_width  = 400;
    int    image_height = int(image_width / aspect_ratio);

    // ── 씬 구성 ─────────────────────────────────────────────────
    // 작은 구 + 거대한 땅 구 — 두 구 모두 동일한 hit() 인터페이스로 처리됨
    hittable_list world;
    world.add(make_shared<sphere>(point3( 0,    0,   -1), 0.5));    // 정면의 작은 구
    world.add(make_shared<sphere>(point3( 0, -100.5, -1), 100));    // 거대한 땅 구

    // ── 카메라 / 뷰포트 설정 ─────────────────────────────────────
    double focal_length    = 1.0;
    double viewport_height = 2.0;
    double viewport_width  = viewport_height * aspect_ratio;
    point3 camera_origin(0, 0, 0);

    vec3 viewport_u(viewport_width,  0, 0);
    vec3 viewport_v(0, -viewport_height, 0);
    vec3 pixel_delta_u = viewport_u / image_width;
    vec3 pixel_delta_v = viewport_v / image_height;

    point3 viewport_upper_left =
        camera_origin - vec3(0, 0, focal_length) - viewport_u/2 - viewport_v/2;
    point3 pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v);

    // ── 렌더링 ───────────────────────────────────────────────────
    std::filesystem::create_directories("output");
    std::ofstream out("output/ch5_normals.ppm");
    if (!out) { std::cerr << "Failed to open output file\n"; return 1; }

    out << "P3\n" << image_width << ' ' << image_height << "\n255\n";

    for (int j = 0; j < image_height; j++)
    {
        std::clog << "\rScanlines remaining: " << (image_height - j) << "  " << std::flush;
        for (int i = 0; i < image_width; i++)
        {
            point3 pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v);
            ray r(camera_origin, pixel_center - camera_origin);
            write_color(out, ray_color(r, world));
        }
    }

    std::clog << "\rDone.               \n";
    return 0;
}
