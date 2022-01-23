#!/bin/env python3

# See https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html

import sys, os.path
import cv2 as cv
import logging as log
import numpy as np
from enum import Enum
from math import atan2, sqrt, cos, sin, radians

pagenr = 2

class Line():
    def __init__(self, line):
        self._line = line
        self.x1, self.y1, self.x2, self.y2 = line
        self.color = (0,0,0,0)
        self.distance = self.calcDistance(line)
        self.angleDeg = self.calcAngleDeg(line)
        self.angleRad = self.calcAngleRad(line)
        self.width = 1

    def __str__(self):
        return "{} -> x1: {}, y1: {}, x2: {}, y2: {}, distance: {}, angle: {}, color: {}, width: {}".format(type(self).__name__, self.x1, self.y1, self.x2, self.y2, self.distance, self.angleDeg, self.color, self.width)

    @property
    def line(self):
        return (self.x1, self.y1, self.x2, self.y2)

    @staticmethod
    def calcDistance(line):
        x1, y1, x2, y2 = line
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def calcAngleDeg(line):
        x1, y1, x2, y2 = line
        return atan2(y2 - y1, x2 - x1) * 180.0 / np.pi

    @staticmethod
    def calcAngleRad(line):
        x1, y1, x2, y2 = line
        return atan2(y1 - y2, x1 - x2)

    @staticmethod
    def calcPointDinstance(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def calcucatePoint(point, angleRad, distance):
        return (int(point[0] - distance * cos(angleRad)), int(point[1] - distance * sin(angleRad)))

    def p1(self):
        return (self.x1, self.y1)

    def p2(self):
        return (self.x2, self.y2)

    @property
    def bottom(self):
        if self.x1 >= self.x2 and self.y1 >= self.y2:
            return (self.x2, self.y2)
        else:
            return (self.x1, self.y1)

    @property
    def top(self):
        if self.x1 <= self.x2 and self.y1 <= self.y2:
            return (self.x1, self.y1)
        else:
            return (self.x2, self.y2)

    def debugDraw(self, preview):
        x1, y1, x2, y2 = self.line
        log.debug(self)
        cv.line(preview, (x1, y1), (x2, y2), self.color, self.width, cv.LINE_AA)

class Side(Enum):
    NONE = 0
    RECTO = 1
    VERSO = 2

    def __repr__(self):
        return self.name

class Cut(Line):
    def __init__(self, line, size):
        if isinstance(line, Line):
            super().__init__(line.line)
        else:
            raise "No Line provided"

        self.h, self.w = size
        log.debug("Constructing Cut from line {} for dimensions {}".format(line, size))
        distanceTop = Line.calcPointDinstance((self.x2, 0),(self.p2()))
        distanceBottom = Line.calcPointDinstance((self.x1, self.h),(self.x1, self.y1))
        pTop = self.calcucatePoint((self.x2, self.y2), self.angleRad, distanceTop)
        pBottom = self.calcucatePoint((self.x1, self.y1), self.angleRad, -(distanceBottom))

        self.x1, self.y1 = pBottom
        self.x2, self.y2 = pTop
        self.distance = Line.calcDistance(self.line)
        self.color = (255,0,0,255)
        self.width = 3
        if self.x1 < self.w / 2:
            self.side = Side.VERSO
        else:
            self.side = Side.RECTO
        log.debug("Calculated bottom: {}, top {}, side {}".format(pBottom , pTop, self.side))

#https://stackoverflow.com/a/62935825
class Page:
    def __init__(self, file, side):
        self._box = None
        self._nBox = None
        self.side = side
        self._img = cv.imread(file, cv.IMREAD_COLOR)
        self.h, self.w = self._img.shape[:2]
        self.center = (self.w / 2, self.h / 2)
        self._lines = None
        self._preview = None
        self._cut = None
        self.color = (0, 255, 255, 255)
        self.width = 3
        self.fitBox = True
        self.margin = 5

    def findLines(self):
        if self._img.ndim == 2:
             dst = np.copy(self._img)
        else:
            dst = cv.cvtColor(self._img, cv.COLOR_RGB2BGR)
        self._lines = []
        #dst = cv.Canny(src, 50, 200, None, 3)
        dst = cv.Canny(dst, 30, 120, None, 3)
        minLineLength = self.h / 1.2
        maxLineGap = self.h / 4
        for l in cv.HoughLinesP(dst, 5, np.pi / 180, 50, None, minLineLength, maxLineGap):
            self.lines.append(Line(l[0]))
        return self

    def findEdges(self):
        if self._lines == None:
            self.findLines()
        dst = np.copy(self._img)
        dst = cv.Canny(dst, 80, 100, None, 3)
        minLineLength = self.w / 1.2
        maxLineGap = self.w / 8
        cv.imshow("Binary page view", dst)
        cv.waitKey()

    @property
    def src(self):
        return self._img

    @property
    def lines(self):
        if self._lines == None:
            self.findLines()
        return self._lines

    @property
    def cut(self):
        if self._cut == None:
            self.findCut()
        return self._cut

    @property
    def box(self):
        if self._box == None:
            self.calculateBox()
        return self._box

    @property
    def preview(self):
        if not(isinstance(self._preview, np.ndarray)) or self._preview == None:
            self._preview = cv.cvtColor(self._img, cv.COLOR_RGB2RGBA)
        return self._preview

    def debugColorize(self):
        if len(self._lines) > 0:
            color = 255
            for line in sorted(filter(lambda line: line.x1 < self.w / 2, self._lines), key=lambda line: line.distance, reverse=False):
                line.color = (0, 0, color, color)
                color = color - 20

            color = 255
            for line in sorted(filter(lambda line: line.x1 > self.w / 2, self._lines), key=lambda line: line.distance, reverse=False):
                line.color = (0, color, 0, color)
                color = color - 20
        return self

    # Filter only vertical lines
    def filter(self, min = -88, max = -92):
        self._lines = list(filter(lambda line: min >= line.angleDeg >= max, sorted(self._lines, key=lambda line: line.x1)))
        return self

    def findCut(self):
        if not(isinstance(self._lines, list)) and self._lines == None:
            self.findLines()
        if len(self._lines) == 0:
            raise "No lines found"
        if self.side == Side.VERSO:
        #Fold left
            leftLines = list(sorted(filter(lambda line: line.x1 < self.w / 2, self._lines), key=lambda line: line.distance, reverse=False))
            self._cut = Cut(leftLines[0], (self.h, self.w))
        else:
        #Fold right
            rightLines = list(sorted(filter(lambda line: line.x1 > self.w / 2, self._lines), key=lambda line: line.distance, reverse=False))
            self._cut = Cut(rightLines[0], (self.h, self.w))
        if log.root.level == log.DEBUG:
            self._lines.append(self._cut)
        return self

    def margin(self):
        if self.side == Side.RECTO:
            self._cut.x1 -= self.margin
            self._cut.x2 -= self.margin
        else:
            self._cut.x1 += self.margin
            self._cut.x2 += self.margin

    def calculateBox(self):
        if self._cut == None:
            self.findCut()
        w = self.w
        if self._cut.bottom[0] < self._cut.top[0]:
            w = w - self._cut.top[0]
        else:
            w = w - self._cut.bottom[0]
        if self.side == Side.RECTO:
            w = -(self.w - w)

        angle = self._cut.angleRad + radians(90)

        log.debug("Calculating box with width {}, angle {} (radians)".format(w, angle))
        if self.fitBox == False:
            pTop = Line.calcucatePoint((self._cut.top[0], self._cut.top[1]), angle, w)
            pBottom = Line.calcucatePoint((self._cut.bottom[0], self._cut.bottom[1]), angle, w)
            self._box = ((self._cut.top[0], self._cut.top[1]),  (pTop), (pBottom), (self._cut.bottom[0], self._cut.bottom[1]))
        else:
            if self._cut.angleDeg > - 90:
            #tilted to the right, lower initial point need to be ajusted to fit the page
                pTop = Line.calcucatePoint((self._cut.top[0], self._cut.top[1]), angle, w)
                pBottom = Line.calcucatePoint((pTop), self._cut.angleRad, -(self.h - pTop[1]))
                npBottom = Line.calcucatePoint((pBottom), angle, -(w))
                self._box = ((self._cut.top[0], self._cut.top[1]),  (pTop), (pBottom), (npBottom))
            else:
            #tilted to the left, upper initial point need to be ajusted to fit the page
                pBottom = Line.calcucatePoint((self._cut.bottom[0], self._cut.bottom[1]), angle, w)
                pTop = Line.calcucatePoint((pBottom), self._cut.angleRad, -(self.h - pBottom[1]))
                npTop = Line.calcucatePoint((pTop), angle, -(w))
                self._box = ((npTop),  (pTop), (pBottom), (self._cut.bottom[0], self._cut.bottom[1]))
        self._nBox = list(self._box)
        for i,coord in enumerate(self._box):
             matrix = cv.getRotationMatrix2D((self.center), self._cut.angleDeg + 90, 1.0)
             cos = np.abs(matrix[0, 0])
             sin = np.abs(matrix[0, 1])
             v = [coord[0],coord[1],1]
             calculated = np.dot(matrix, v)
             log.debug("Matrix is {}, v is {}, dot product is {}".format(matrix, v, calculated))
             self._nBox[i] = (int(calculated[0]),int(calculated[1]))
        return self

    @property
    def rotated(self):
        if self._nBox == None:
            self.calculateBox()
        matrix = cv.getRotationMatrix2D(self.center, self._cut.angleDeg + 90, 1.0)
        (x1, y1), (x2, y2) = self._nBox[0], self._nBox[2]
        log.debug("extracting at {} -> {}".format((x1, y1), (x2, y2)))
        return cv.warpAffine(self._img, matrix, (self.w, self.h), flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)[y1:y2, x1:x2, :]

    def debugDraw(self, preview = None):
        if not(isinstance(preview, np.ndarray)) or preview.size == 0:
            log.debug("Creating empty preview!")
            preview = self.preview
        for i in range(len(self.box)-1):
            p1 = (self.box[i][0], self.box[i][1])
            p2 = (self.box[i+1][0],self.box[i+1][1])
            log.debug("Drawing line {} from {} to {}".format(i, p1, p2))
            cv.line(preview, (p1), (p2), (self.color), self.width)
        log.debug("Drawing line from {} to {}".format((self.box[3][0], self.box[3][1]), (self.box[0][0], self.box[0][1])))
        cv.line(preview, (self.box[3][0], self.box[3][1]), (self.box[0][0], self.box[0][1]), (self.color), self.width)
        self._cut.width = 2
        self._cut.color = (255,0,0,127)
        self._cut.debugDraw(preview)

    def debugRotate(self):
        preview = cv.cvtColor(self._img, cv.COLOR_RGB2RGBA)
        matrix = cv.getRotationMatrix2D(self.center, self._cut.angleDeg + 90, 1.0)
        #log.debug("Matrix is {}".format(matrix))
        preview = cv.warpAffine(preview, matrix, (self.w, self.h), flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)
        for i in range(len(self._nBox)-1):
            p1 = (self._nBox[i][0], self._nBox[i][1])
            p2 = (self._nBox[i+1][0],self._nBox[i+1][1])
            log.debug("Drawing line {} from {} to {}".format(i, p1, p2))
            cv.line(preview, (p1), (p2), (self.color), self.width)
        log.debug("Drawing line from {} to {}".format((self._nBox[3][0], self._nBox[3][1]), (self._nBox[0][0], self._nBox[0][1])))
        cv.line(preview, (self._nBox[3][0], self._nBox[3][1]), (self._nBox[0][0], self._nBox[0][1]), (self.color), self.width)
        return preview

    @staticmethod
    def absBox(box):
        return (box[0], box[1], box[0] + box[3], box[1] + box[2])


def addSides(fileList):
    files = {}
    for i in range(len(fileList)):
        if i == 0:
            files[fileList[i]] = Side.NONE
        elif (i % 2) == 0:
        #Fold left
            files[fileList[i]] = Side.VERSO
        else:
        #Fold right
            files[fileList[i]] = Side.RECTO
    return files

def debugDraw(preview, shapes):
    for shape in shapes:
        debugDraw = getattr(shape, "debugDraw", None)
        if callable(debugDraw):
            shape.debugDraw(preview)
        else:
            log.debug("Class {} has no debugDraw method!", type(shape).__name__)
    return preview

def main():
    log.basicConfig(level=log.DEBUG)

    index = pagenr - 1
    file, side = list(files.keys())[index], list(files.values())[index]
    if os.path.isfile(file):
        page = Page(file, side)
    else:
        print("File {} not found, exiting!".format(file))
        sys.exit(1)

    page.findLines().filter().debugColorize().findCut().calculateBox()
    page.findEdges()
#
    preview, rotated, box = None, None, None
    if log.root.level == log.DEBUG:
        preview = debugDraw(page.preview, page.lines)
        page.debugDraw(preview)
        rotated = page.debugRotate()

    cv.imshow("Source", page.src)
    cv.imshow("Target", page.rotated)

    if rotated is not None:
        cv.imshow("rotated", rotated )
    if box is not None:
        cv.imshow("box", box )
    if preview is not None:
        cv.imshow("Detected Lines (in red and green), detected fold (in blue)", preview)

    log.debug("Processed {}, side {}".format(file, repr(side)))
    cv.waitKey()


if __name__ == '__main__':
    files = addSides(['./data/DE-611-HS-3461927/00000001.jpg', './data/DE-611-HS-3461927/00000002.jpg', './data/DE-611-HS-3461927/00000003.jpg', './data/DE-611-HS-3461927/00000004.jpg', './data/DE-611-HS-3461927/00000005.jpg', './data/DE-611-HS-3461927/00000006.jpg', './data/DE-611-HS-3461927/00000007.jpg'])

    main()
