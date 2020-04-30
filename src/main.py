import numpy as np
import cv2
import 基于opencv的木质缺陷识别分类.Products as product

# 加载视频
cap = cv2.VideoCapture("../sample/1.mp4")

# 变量
font = cv2.FONT_HERSHEY_SIMPLEX
products = []
pid = 1
areaTh = 18000
# 获取图像width, height
width = cap.get(3)
height = cap.get(3)

while cap.isOpened():
    ret, frame = cap.read()

    try:
        # 复制图片，用于绘制
        img = frame.copy()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]

    except:
        print("EOF")
        break

    # 边缘检测，识别工件
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > areaTh:
            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            x, y, w, h = cv2.boundingRect(cnt)
            new = True
            if cx > 100:
                for i in products:
                    if abs(cx - i.getX()) <= 25 and abs(cy - i.getY()) <= 25:
                        new = False
                        i.updateCoords(cx, cy, x, y, w, h)
                if new:
                    p = product.Product(pid, cx, cy, x, y, w, h)
                    p.save_pic(frame)
                    products.append(p)
                    product.count = pid
                    defects = p.defect_detect()
                    pid += 1
                cv2.circle(img, (cx, cy), 5, (0, 0, 255), -1)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    for i in products:
        # 标记ID
        if i.getX() <= 600:
            cv2.putText(img, str(i.getId()), (i.getX(), i.getY()), font, 1.0, i.getRGB(), 1, cv2.LINE_AA)

            # 绘制缺陷
            for j in i.defects:
                if j.getState() == 1:
                    img = cv2.rectangle(img, (i.getBoundX() + j.getX(), i.getBoundY() + j.getY()),
                                        (i.getBoundX() + j.getX() + j.getW() + 5,
                                         i.getBoundY() + j.getY() + j.getH() + 5),
                                        (0, 255, 255),
                                        1)
                elif j.getState() == 2:
                    img = cv2.rectangle(img, (i.getBoundX() + j.getX(), i.getBoundY() + j.getY()),
                                        (i.getBoundX() + j.getX() + j.getW() + 5,
                                         i.getBoundY() + j.getY() + j.getH() + 5),
                                        (255, 255, 0),
                                        1)
        # 绘制sum
        cv2.putText(img, "sum:" + str(product.count), (10, 30), font, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img, "scratch_sum:" + str(product.Product.scratch_sum), (10, 50), font, 0.7, (0, 255, 255), 1,
                    cv2.LINE_AA)
        cv2.putText(img, "blot_sum:" + str(product.Product.blot_sum), (10, 70), font, 0.7, (255, 255, 0), 1,
                    cv2.LINE_AA)
    cv2.imshow("test", img)
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()
