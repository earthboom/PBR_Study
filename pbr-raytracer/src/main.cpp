#include <iostream>
#include <fstream>
#include <filesystem>

#include "vec3.h"

// color 값을 PPM 포맷으로 파일에 출력한다.
// color의 각 채널은 0.0~1.0 실수이므로 255를 곱해 정수로 변환한다.
void write_color(std::ostream& out, const color& pixel_color)
{
    int ir = int(255.999 * pixel_color.x());
    int ig = int(255.999 * pixel_color.y());
    int ib = int(255.999 * pixel_color.z());
    out << ir << ' ' << ig << ' ' << ib << '\n';
}

int main()
{
    const int image_width  = 256;
    const int image_height = 256;

    std::filesystem::create_directories("output");
    std::ofstream out("output/first_image.ppm");
    if (!out) { std::cerr << "Failed to open output file\n"; return 1; }

    // PPM 헤더: 포맷(P3), 해상도, 최대 색상값
    out << "P3\n" << image_width << ' ' << image_height << "\n255\n";

    for (int j = 0; j < image_height; j++)
    {
        std::clog << "\rScanlines remaining: " << (image_height - j) << "  " << std::flush;
        for (int i = 0; i < image_width; i++)
        {
            // 픽셀 좌표를 0.0~1.0 으로 정규화하여 색상으로 사용
            color pixel_color(
                double(i) / (image_width  - 1),  // R: 왼쪽→오른쪽
                double(j) / (image_height - 1),  // G: 위→아래
                0.0                               // B: 고정
            );
            write_color(out, pixel_color);
        }
    }

    std::clog << "\rDone.               \n";
    return 0;
}
