
@Grab(group='org.openpnp', module='opencv', version='4.5.1-2')

import nu.pattern.OpenCV
import org.opencv.core.*
import org.opencv.highgui.HighGui
import org.opencv.imgcodecs.Imgcodecs


OpenCV.loadShared();

def colors = Arrays.asList(new Scalar(127,127,127), new Scalar(0,0,255), new Scalar(0,255,0), new Scalar(255,0,0), new Scalar(255,255,0), new Scalar(255,0,255), new Scalar(0,255,255), new Scalar(255,255,255), new Scalar(0,0,0))

List<Mat> fields = []

for (color in colors) {
    Mat test = new Mat(100, 100, CvType.CV_8UC3)
    test.setTo(color)
    fields.add(test)
}

List<Mat> rows = []
for (i = 0; i < Math.sqrt(fields.size()); i++) {
    Mat dst = new Mat()
    List<Mat> src = fields[Math.sqrt(fields.size())*i..Math.sqrt(fields.size())*(i+1)-1]
    Core.hconcat(src, dst)
    rows.add(dst)
}

Mat testpattern = new Mat()
Core.vconcat(rows, testpattern)

//def file = "../../coins/data/record_DE-MUS-062622_kenom_127703/rs.jpg"
//Mat mat = Imgcodecs.imread(file, Imgcodecs.IMREAD_UNCHANGED)
HighGui.imshow("Test pattern", testpattern)
HighGui.waitKey()