
import numpy as np
import cv2 as cv

def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step / 2:h:step, step / 2:w:step].reshape(2, -1).astype(int)
    fx, fy = flow[y, x].T
    lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    cv.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        cv.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis

def warp_flow(img, flow):
    h, w = flow.shape[:2]
    #flow = -flow
    flow[:, :, 0] += np.arange(w)
    flow[:, :, 1] += np.arange(h)[:, np.newaxis]
    res = cv.remap(img, flow, None, cv.INTER_LINEAR)
    return res

def run_opical_flow():
    #이미지 불러오기
    prev_img = cv.imread("prev.tiff", cv.IMREAD_ANYDEPTH)
    next_img = cv.imread("next.tiff", cv.IMREAD_ANYDEPTH)
   # assert (prev_img != None and next_img != None)

    #테스트를 위한 x로 10 이동한 이미지 생성
    # h, w = prev_img.shape[:2]
    # M = np.float_([[1, 0, 10], [0, 1, 0]])
    # test_next_img = cv.warpAffine(prev_img, M, (w, h))
    # cv.imshow("img", test_next_img)

    # optical flow 계산
    win_size = 5
    iteration = 5
    flow = cv.calcOpticalFlowFarneback(prev_img, next_img, None, 0.5, 3, win_size, iteration, 5, 1.2, 0)

    #플로우 그리기
    # vis = draw_flow(prev_img, flow, 15)
    cv.imshow("prev_img", prev_img)
    cv.imshow("next_img", next_img)

    # calculated_prev_img 계산
    interpolation = True
    calculated_prev_img = np.zeros_like(next_img)
    if interpolation == True:
        calculated_prev_img = warp_flow(next_img, flow)
    else:
        calculated_prev_img = calculated_prev_img + 0.5
        for xx in range(next_img.shape[1]):
            for yy in range(next_img.shape[0]):
                flowed_xx = int(xx - flow[yy, xx, 0])
                flowed_yy = int(yy - flow[yy, xx, 1])
                # next이미지의 픽셀값을 calculated prev 이미지에다가 넣음(중복된 픽셀이동에 걍 겹처버림)
                if 0 < flowed_xx < next_img.shape[1] and 0 < flowed_yy < next_img.shape[0]:
                    calculated_prev_img[flowed_yy, flowed_xx] = next_img[yy, xx]

    #결과 display
    cv.imshow("cal_prev_img", calculated_prev_img)
    cv.imwrite("cal_prev_img.tiff", calculated_prev_img)
    cv.waitKey(0)

    #save
    cv.imwrite("result_img.tiff", calculated_prev_img)
    



# #op.run_opical_flow()

# img_prev = cv.imread("prev.tiff", cv.IMREAD_ANYDEPTH)
# img_next = cv.imread("next.tiff", cv.IMREAD_ANYDEPTH)

# map_x = cv.imread("displacement_x.tif", cv.IMREAD_ANYDEPTH)
# map_y = cv.imread("displacement_y.tif", cv.IMREAD_ANYDEPTH)

# for i in range(map_x.shape[1]):
#     map_x[:, i] += i

# for j in range(map_y.shape[0]):
#     map_y[j, :] += j

# cv.imshow("prev img", img_prev)
# cv.imshow("next img", img_next)

# img_result = cv.remap(img_next, map_x, map_y, cv.INTER_LINEAR)
# cv.imshow("result.tiff", img_result)
# cv.imwrite("result.tiff", img_result)

# cv.waitKey(0)


# # img_one_partical = cv.imread("test_oneParticle.tif", cv.IMREAD_ANYDEPTH)
# #
# # map_x = np.zeros((img_one_partical.shape[0], img_one_partical.shape[1]), dtype=np.float32)
# # map_y = np.zeros((img_one_partical.shape[0], img_one_partical.shape[1]), dtype=np.float32)
# #
# # for i in range(map_x.shape[1]):
# #     map_x[:, i] = i
# # for j in range(map_y.shape[0]):
# #     map_y[j, :] = j
# #
# #
# # img_result = cv.remap(img_one_partical, map_x, map_y, cv.INTER_LINEAR)
# #
# # cv.imshow("img_one_partical_rs", img_one_partical)
# # cv.imshow("img_one_result_rs", img_result)
# #
# # cv.imwrite("img_result.tiff", img_result)
# #
# # cv.waitKey(0)