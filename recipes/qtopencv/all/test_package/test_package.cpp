#include <QImage>
#include <cvmatandqimage.h>
#include <opencv2/core/core.h>

auto main() -> int {
  QImage image{};
  [[maybe_unused]] cv::Mat mat{image2Mat(image)};
}