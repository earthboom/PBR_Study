#include <fstream>
#include <filesystem>

#include "rtweekend.h"
#include "hittable_list.h"
#include "sphere.h"
#include "camera.h"
#include "material.h"

int main()
{
    // ── 재질 정의 ────────────────────────────────────────────────
    auto mat_ground = make_shared<lambertian>(color(0.8, 0.8, 0.0)); // 노란 땅
    auto mat_center = make_shared<lambertian>(color(0.1, 0.2, 0.5)); // 파란 확산 구
    auto mat_left   = make_shared<dielectric>(1.50);                  // 유리 (굴절률 1.5)
    auto mat_bubble = make_shared<dielectric>(1.00 / 1.50);           // 속 빈 유리 내부 공기
    auto mat_right  = make_shared<metal>(color(0.8, 0.6, 0.2), 0.0); // 완벽한 금색 금속

    // ── 씬 구성 ─────────────────────────────────────────────────
    hittable_list world;
    world.add(make_shared<sphere>(point3( 0.0, -100.5, -1.0), 100.0, mat_ground));
    world.add(make_shared<sphere>(point3( 0.0,    0.0, -1.2),   0.5, mat_center));
    world.add(make_shared<sphere>(point3(-1.0,    0.0, -1.0),   0.5, mat_left));
    world.add(make_shared<sphere>(point3(-1.0,    0.0, -1.0),  -0.4, mat_bubble));
    world.add(make_shared<sphere>(point3( 1.0,    0.0, -1.0),   0.5, mat_right));

    // ── 카메라 설정 ──────────────────────────────────────────────
    camera cam;
    cam.aspect_ratio      = 16.0 / 9.0;
    cam.image_width       = 400;
    cam.samples_per_pixel = 100;
    cam.max_depth         = 50;

    cam.vfov     = 20;                       // 좁은 시야각 — 씬이 확대되어 보임
    cam.lookfrom = point3(3, 3, 2);          // 오른쪽 위 대각선에서 내려다보는 위치
    cam.lookat   = point3(0, 0, -1);         // 씬 중심을 바라봄
    cam.vup      = vec3(0, 1, 0);            // 월드 위쪽

    // ── 렌더링 ───────────────────────────────────────────────────
    const std::filesystem::path out_dir = std::filesystem::path(PROJECT_SOURCE_DIR) / "output";
    std::filesystem::create_directories(out_dir);
    std::ofstream out(out_dir / "ch10_camera.ppm");
    if (!out) { std::cerr << "Failed to open output file\n"; return 1; }

    cam.render(world, out);
    return 0;
}
