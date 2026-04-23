#include <iostream>
#include <fstream>
#include <filesystem>
#include <cmath>

#include "vec3.h"
#include "ray.h"

void write_color(std::ostream& out, const color& pixel_color)
{
    int ir = int(255.999 * pixel_color.x());
    int ig = int(255.999 * pixel_color.y());
    int ib = int(255.999 * pixel_color.z());
    out << ir << ' ' << ig << ' ' << ib << '\n';
}

// 광선이 구에 맞는지 판별하고, 맞으면 교차점의 t값을 반환한다.
// 맞지 않으면 -1.0 반환.
//
// 수학적 유도:
//   구의 방정식: |P - C|² = r²  (C=중심, r=반지름)
//   광선 대입:   |A + t*b - C|² = r²
//   전개:        t²|b|² + 2t(b·(A-C)) + |A-C|²-r² = 0
//
//   이차방정식 at² + 2ht + c = 0  (h = b·(A-C) 로 치환)
//   판별식 = h² - a*c
//     < 0 : 교차 없음
//     = 0 : 접선 (1점)
//     > 0 : 2점 교차 → 가까운 쪽 t 반환
double hit_sphere(const point3& center, double radius, const ray& r)
{
    vec3 oc = center - r.origin();         // (C - A)
    double a = dot(r.direction(), r.direction());
    double h = dot(r.direction(), oc);     // h = b·(C-A), 부호 반전 편의상
    double c = dot(oc, oc) - radius * radius;
    double discriminant = h*h - a*c;

    if (discriminant < 0)
        return -1.0;                       // 교차 없음

    // 가장 가까운 교차점 (작은 t값)
    return (h - std::sqrt(discriminant)) / a;
}

color ray_color(const ray& r)
{
    // 구: 중심 (0, 0, -1), 반지름 0.5
    double t = hit_sphere(point3(0, 0, -1), 0.5, r);

    if (t > 0.0)
    {
        // 교차점의 법선 벡터 계산: 교차점 - 구 중심, 정규화
        // 법선을 색상으로 시각화 (-1~1 범위 → 0~1 범위로 변환)
        vec3 normal = unit_vector(r.at(t) - vec3(0, 0, -1));
        return 0.5 * color(normal.x()+1, normal.y()+1, normal.z()+1);
    }

    // 배경: 하늘 그라디언트
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
    std::ofstream out("output/ch4_sphere.ppm");
    if (!out) { std::cerr << "Failed to open output file\n"; return 1; }

    out << "P3\n" << image_width << ' ' << image_height << "\n255\n";

    for (int j = 0; j < image_height; j++)
    {
        std::clog << "\rScanlines remaining: " << (image_height - j) << "  " << std::flush;
        for (int i = 0; i < image_width; i++)
        {
            point3 pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v);
            ray r(camera_origin, pixel_center - camera_origin);
            write_color(out, ray_color(r));
        }
    }

    std::clog << "\rDone.               \n";
    return 0;
}
