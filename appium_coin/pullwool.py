from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os,time,random,winsound
# 微鲤看看配置信息
loadingTime = 8 # APP加载时间
startRandom = 20 # 拖动次数下限，上限
endRandom = 25
watchNewsCount = 600 # 查看新闻个数
scrollTime = 500 # 展开文章后，每次滚动时间配置
newsRunTime = 10 # 看新闻总时间，分钟计时
videosRunTime = 10 # 看视频总时间，分钟计时
videosWatch = 1.5 # 看单个视频时间，分钟计时
# 趣头条配置信息
qttStartRandom = 30
qttEndRandom = 40
qttRunTime = 20
qttVideosWatch = 2
# 聚看点配置信息
jkdNewsRunTime = 20
jkdVideosRunTime = 20
jkdVideosWatch = 1.5
# 趣看天下配置信息
qktxNewsRunTime = 20
qktxVideoTime = 2
# 所有app运行循环次数
runCount = 3

deviceName = '812d234b' # 手机设备号：cfc4c454,812d234b,68U5T18315002011
platformVersion = '8.0.0' # Android手机版本
appName = ['weilikankan.apk','qutoutiao.apk','jukandian.apk','qukantianxia.apk']
appPackage = ['cn.weli.story','com.jifen.qukan','com.xiangzi.jukandian','com.yanhui.qktx']
appActivity = ['cn.etouch.ecalendar.LoadingActivity','com.jifen.qkbase.main.MainActivity',
               'com.xiangzi.jukandian.activity.V2WelcomeActivity',
               'com.yanhui.qktx.activity.SplashActivity']

def signIn(): # 微鲤看看：左上角金币领取
    while True:
        try:
            coinsClick = driver.find_element_by_id('cn.weli.story:id/rl_back_calendar_root')
            goldCoin = coinsClick.find_elements_by_class_name('android.widget.RelativeLayout')
            signIn = goldCoin[0].find_element_by_class_name('android.widget.TextView')
            if '签到' in signIn.text:
                goldCoin[0].click()
                time.sleep(1)
                # driver.find_element_by_class_name('android.widget.Button').click()
                driver.find_element_by_xpath("//android.widget.Button[@text='立即签到']").click()
                time.sleep(1)
                driver.find_element_by_id('cn.weli.story:id/iv_back').click()
            elif '领红包' in signIn.text:
                goldCoin[0].click()
                time.sleep(1)
            elif '+' in signIn.text:
                goldCoin[0].click()
        except Exception or NoSuchElementException:
            windowCheck()
        else:
            break

def bulletBox(resourceId, textViewId): # 微鲤看看：弹框统一处理
    try:
        success = False
        bulletbox = driver.find_elements_by_id('cn.weli.story:id/' + resourceId)
        if len(bulletbox) > 0:
            button = bulletbox[0].find_elements_by_class_name('android.widget.Button')
            textOk = bulletbox[0].find_elements_by_id('cn.weli.story:id/' + textViewId)
            icClose = bulletbox[0].find_elements_by_id('cn.weli.story:id/ic_close')
            if len(button) > 0:
                button[0].click()
                success = True
            elif len(textOk) > 0:
                textOk[0].click()
                success = True
            elif len(icClose)>0:
                icClose[0].click()
                success = True
        return success
    except Exception or NoSuchElementException:
        pass

def rlDialog(): # 微鲤看看：两个弹窗处理
    try:
        success = False
        dialog = driver.find_elements_by_id('cn.weli.story:id/rl_dialog')
        if len(dialog) > 0:
            moneyTake = dialog[0].find_elements_by_id('cn.weli.story:id/iv_take')
            if len(moneyTake) > 0:
                moneyTake[0].click()
                time.sleep(1)
                dialog2 = driver.find_elements_by_id('cn.weli.story:id/rl_dialog2')
                time.sleep(1)
                if len(dialog2) > 0:
                    driver.find_element_by_id('cn.weli.story:id/iv_close').click()
                    success = True
        return success
    except Exception or NoSuchElementException:
        pass

def windowCheck(): # 微鲤看看：总弹窗判断，处理
    isWindow = False
    success  = bulletBox('rl_content', 'text_ok')
    success1 = bulletBox('content', 'bt_ok')
    success2 = bulletBox('ll_layout', 'tv_positive')
    success4 = bulletBox('rl_dialog','ic_close')
    success3 = rlDialog()
    if success == True or success1 == True or success2 == True or success3 == True or success4 == True:
        isWindow = True
    return isWindow

def categoryClick(): # 微鲤看看：每次启动应用点击推荐
    try:
        menu = driver.find_element_by_id('cn.weli.story:id/indicator')
        menuList = menu.find_elements_by_class_name('android.widget.TextView')
        time.sleep(1)
        menuList[0].click()
    except Exception or NoSuchElementException:
        windowCheck()
    else:
        pass

def timeOutCheck(): # 微鲤看看：新闻详情页，金币达到上限验证
    while True:
        try:
            success = False
            # coinLayout = driver.find_element_by_id('cn.weli.story:id/rl_read_coin')
            # timeOut = coinLayout.find_elements_by_class_name('android.widget.TextView')
            timeOut = driver.find_elements_by_id('cn.weli.story:id/tv_read_tips')
            if len(timeOut) > 0:
                success = True
            # coinLayout = driver.find_element_by_id('cn.weli.story:id/rl_read_coin').get_attribute('focusable')
            # if coinLayout == True:
            #     success = True
            return success
        except Exception or NoSuchElementException:
            windowCheck()
        else:
            break

def backNews(): # 微鲤看看：回到新闻列表页
    while True:
        news = driver.find_elements_by_id('cn.weli.story:id/indicator')
        if len(news) == 0:
            driver.back()
        else:
            break
def backVideos(): # 回到视频列表页
    while True:
        videoMenu = driver.find_elements_by_id('cn.weli.story:id/rl_bottom_1')
        videos = driver.find_elements_by_id('cn.weli.story:id/tab_layout')
        if len(videoMenu) == 0:
            driver.back()
        elif len(videos) == 0 and len(videoMenu) != 0:
            videoMenu[0].click()
        else:
            break

def weiliWatchNews(): # 微鲤看看：看新闻
    print("开始看新闻，运行时间:", newsRunTime)
    timeOut = True
    startTime = int(time.time())
    while timeOut:
        try:
            driver.find_element_by_id('cn.weli.story:id/rl_bottom_4').click()
            time.sleep(1)
            etAd = driver.find_elements_by_id('cn.weli.story:id/et_ad')
            if len(etAd)>0:
                time.sleep(1)
                driver.find_element_by_id('cn.weli.story:id/image_close').click()
            todayCoin = driver.find_element_by_id('cn.weli.story:id/text_today_coin')
            print("金币数量为：",int(todayCoin.text))
            if int(todayCoin.text)<5500:
                driver.find_element_by_id('cn.weli.story:id/rl_bottom_1').click()
                time.sleep(1)
                categoryClick()
                for i in range(0, watchNewsCount):
                    endTime = int(time.time())
                    if endTime < (startTime + newsRunTime * 60):
                        view = driver.find_elements_by_id('cn.weli.story:id/recyclerView')
                        viewList = view[0].find_elements_by_id('cn.weli.story:id/layout')
                        # viewList1 = view.find_elements_by_id('cn.weli.story:id/layout_more')
                        ads = viewList[1].find_elements_by_id('cn.weli.story:id/tv_subtitle')
                        if len(ads) > 0:
                            driver.swipe(0, 900, 0, 220,500)
                            time.sleep(1)
                            continue
                        viewList[1].click()
                        if windowCheck() == False:
                            # 展开全文实现方法
                            while True:
                                driver.swipe(0, 900, 0, 220, 500)
                                time.sleep(1)
                                windowCheck()
                                scrollView = driver.find_element_by_id('cn.weli.story:id/scrollview')
                                # 展开全文定位
                                expandText = scrollView.find_elements_by_id('cn.weli.story:id/tv_height_more')
                                if len(expandText) > 0:
                                    expandText[0].click()
                                    scrollCount = random.randint(startRandom, endRandom)
                                    for h in range(0, scrollCount):
                                        if timeOutCheck() == True:
                                            break
                                        driver.swipe(0, 400, 0, 220, scrollTime)
                                        time.sleep(1)
                                        windowCheck()
                                    break
                        time.sleep(1)
                        driver.find_element_by_id('cn.weli.story:id/btn_back').click()
                        time.sleep(1)
                        signIn()
                        driver.swipe(0, 900, 0, 220, 500)
                        time.sleep(1)
                    else:
                        timeOut = False
                        break
        except Exception or NoSuchElementException:
            print("看新闻出现异常，重新启动ing---")
            windowCheck()
            backNews()
        else:
            break


def weiliWatchVideos(): # 微鲤看看：刷视频
    print("开始看视频，运行时间:", videosRunTime)
    timeOut = True
    startTime = int(time.time())
    while timeOut:
        try:
            # driver.find_element_by_id('cn.weli.story:id/rl_bottom_1').click()
            # time.sleep(0.5)
            # signIn()
            windowCheck()
            driver.find_element_by_id('cn.weli.story:id/rl_bottom_2').click()
            time.sleep(0.5)
            listView = driver.find_element_by_id('cn.weli.story:id/listview')
            videosList = listView.find_elements_by_id('cn.weli.story:id/adapter_player_control')
            driver.drag_and_drop(videosList[0], videosList[1])
            for i in range(0, watchNewsCount):
                endTime = int(time.time())
                if endTime < (startTime + videosRunTime * 60):
                    time.sleep(1)
                    listView = driver.find_element_by_id('cn.weli.story:id/listview')
                    videosList = listView.find_elements_by_id('cn.weli.story:id/adapter_player_control')
                    videosList[0].click()
                    videosStart = int(time.time())
                    while True:
                        videosEnd = int(time.time())
                        replay = driver.find_elements_by_id('cn.weli.story:id/premovie_ad_replay')
                        if (len(replay) > 0) or (videosEnd > (videosStart + videosWatch * 60)):
                            # driver.find_element_by_id('cn.weli.story:id/premovie_finish_btn').click()
                            time.sleep(1)
                            break
                    driver.back()
                    driver.swipe(0, 1100, 0, 300, 500)
                else:
                    timeOut = False
                    break
        except Exception or NoSuchElementException:
            print("看视频出现异常，重新启动ing---")
            windowCheck()
            backVideos()
        else:
            break


def qttBackNews():
    while True:
        newsList = driver.find_elements_by_id('com.jifen.qukan:id/x0')
        if len(newsList) != 0:
            break
        else:
            driver.back()
def qttGetCoin():
    getCoin = driver.find_elements_by_id('com.jifen.qukan:id/vo')
    coin = getCoin[0].find_elements_by_id('com.jifen.qukan:id/vu')
    if len(coin) > 0 and ('0' in coin[0].text):
        getCoin[0].click()
    else:
        pass
def qttWindowCheck():
    content = driver.find_elements_by_id('android:id/content')
    close = driver.find_elements_by_id('com.jifen.qukan:id/a02')
    if len(content) > 0 and len(close) > 0:
        close[0].click()
def qttCheckIn():
    driver.find_element_by_id('com.jifen.qukan:id/ju').click()
    time.sleep(2)
    driver.find_element_by_id('com.jifen.qukan:id/jq').click()
def qutoutiao():
    print("看新闻、视频运行时间：", qttRunTime)
    startTime = int(time.time())
    timeOut = True
    while timeOut:
        try:
            qttCheckIn()
            qttGetCoin()
            driver.swipe(0, 800, 0, 220, 500)
            for i in range(0, watchNewsCount):
                endTime = int(time.time())
                if endTime < (startTime + qttRunTime * 60):
                    time.sleep(2)
                    nz = driver.find_element_by_id('com.jifen.qukan:id/nz')
                    layout = nz.find_elements_by_class_name('android.widget.LinearLayout')
                    # ads = layout[0].find_elements_by_id('com.jifen.qukan:id/a6i')
                    # # print(len(layout))
                    # # print(len(ads))
                    # if len(ads) == 1:
                    #     driver.swipe(0, 800, 0, 220, 500)
                    #     time.sleep(1)
                    ads = layout[0].find_elements_by_class_name('android.widget.TextView')
                    for j in range(0,len(ads)):
                        if '广告' in ads[j].text:
                            driver.swipe(0, 800, 0, 220, 500)
                    # else:
                    layout[0].click()
                    qttVideos = driver.find_elements_by_class_name('com.qukan.media.player.renderview.TextureRenderView')
                    if len(qttVideos) > 0:
                        videosStart = int(time.time())
                        while True:
                            videosEnd = int(time.time())
                            clouseAds = driver.find_elements_by_id('com.jifen.qukan:id/nb')
                            if len(clouseAds)>0 or (videosEnd > (videosStart + qttVideosWatch * 60)):
                                break
                    elif len(driver.find_elements_by_id('com.jifen.qukan:id/xk')) > 0:
                        pass
                    else:
                        while True:
                            time.sleep(1)
                            scrollCount = random.randint(qttStartRandom, qttEndRandom)
                            for h in range(0, scrollCount):
                                # if timeOutCheck() == True:
                                #     break
                                driver.swipe(0, 400, 0, 220, scrollTime)
                                while True:
                                    alert = driver.find_elements_by_id('_antispam_dialog_')
                                    if len(alert) > 0:
                                        winsound.PlaySound('Global.wav', winsound.SND_ALIAS)
                                    else:
                                        break
                                time.sleep(1)
                            break
                    time.sleep(1)
                    driver.back()
                    #driver.find_element_by_id('com.jifen.qukan:id/kr').click()
                    time.sleep(1)
                    driver.swipe(0, 800, 0, 220, 500)
                    time.sleep(1)
                else:
                    timeOut = False
                    break
        except Exception or NoSuchElementException:
            print("看新闻出现异常，重新启动ing---")
            qttWindowCheck()
            qttBackNews()
            driver.swipe(0, 700, 0, 220, 500)
        else:
            break
def jkdWindowCheck():
    newsPush = driver.find_elements_by_id('com.xiangzi.jukandian:id/cardview')
    bg = driver.find_elements_by_id('com.xiangzi.jukandian:id/bg')
    if len(bg) > 0:
        bg[0].find_element_by_id('com.xiangzi.jukandian:id/tosign').click()
        time.sleep(2)
        driver.back()
    elif len(newsPush) > 0:
        driver.find_element_by_id('com.xiangzi.jukandian:id/dismisstv').click()
    else:
        pass
def jkdAdsCheck():
    adsRemove = driver.find_elements_by_id('com.xiangzi.jukandian:id/cardview')
    if len(adsRemove) > 0:
        driver.back()
def jkdBackNews():
    while True:
        newsList = driver.find_elements_by_id('com.xiangzi.jukandian:id/ll_tab1_layout')
        if len(newsList) > 0:
            break
        else:
            driver.back()
            time.sleep(2)
def jkdGetCoin():
    getcoin = driver.find_elements_by_id('com.xiangzi.jukandian:id/rl_lingqu_par')
    if len(getcoin) > 0:
        getcoin[0].click()
    time.sleep(1)
    dialogClose = driver.find_elements_by_id('com.xiangzi.jukandian:id/dialog_close')
    imgClose = driver.find_elements_by_id('com.xiangzi.jukandian:id/close_img_layout')
    if len(dialogClose) > 0:
        dialogClose[0].click()
    elif len(imgClose) > 0:
        imgClose[0].click()
def jkdWatchNews():
    print("看新闻运行时间：", jkdNewsRunTime)
    timeOut = True
    startTime = int(time.time())
    while timeOut:
        try:
            jkdWindowCheck()
            jkdGetCoin()
            driver.find_element_by_id('com.xiangzi.jukandian:id/ll_tab3_layout').click()
            time.sleep(2)
            driver.find_element_by_id('com.xiangzi.jukandian:id/ll_tab1_layout').click()
            time.sleep(1)
            driver.find_element_by_id('com.xiangzi.jukandian:id/ll_tab1_layout').click()
            for i in range(0, watchNewsCount):
                endTime = int(time.time())
                if endTime < (startTime + jkdNewsRunTime * 60):
                    jkdWindowCheck()
                    jkdGetCoin()
                    newsWidget = driver.find_element_by_class_name('android.support.v7.widget.RecyclerView')
                    newsList = newsWidget.find_elements_by_class_name('android.widget.LinearLayout')
                    newsAds = newsList[0].find_elements_by_id('com.xiangzi.jukandian:id/item_artical_ad_three_source')
                    baiduAds = newsList[0].find_elements_by_id('com.xiangzi.jukandian:id/item_artical_ad_name2')
                    if len(newsAds) > 0 or len(baiduAds) > 0:
                        driver.swipe(0, 900, 0, 220,500)
                    elif len(newsAds) == 0 and len(baiduAds) == 0:
                        newsList[0].click()
                        time.sleep(1)
                        toobar = driver.find_elements_by_id('com.xiangzi.jukandian:id/toobar_parent')
                        if len(toobar) > 0:
                            scrollCount = random.randint(startRandom, endRandom)
                            for h in range(0, scrollCount):
                                readMore = driver.find_elements_by_xpath("//android.view.View[@text='查看全文，奖励更多']")
                                if len(readMore) > 0:
                                    readMore[0].click()
                                    time.sleep(1)
                                    prClose = driver.find_elements_by_id('com.xiangzi.jukandian:id/preview_close')
                                    if len(prClose) > 0:
                                        prClose[0].click()
                                driver.swipe(0, 400, 0, 220, scrollTime)
                                time.sleep(1.5)
                            driver.back()
                            driver.swipe(0, 900, 0, 220, 500)
                else:
                    timeOut = False
                    break
        except Exception or NoSuchElementException:
            print("看新闻出现异常，重新启动ing---")
            jkdWindowCheck()
            jkdBackNews()
        else:
            break
def jkdWatchVideos(): # 聚看点：刷视频
    print("开始看视频，运行时间:", jkdVideosRunTime)
    timeOut = True
    startTime = int(time.time())
    while timeOut:
        try:
            driver.find_element_by_id('com.xiangzi.jukandian:id/ll_tab1_layout').click()
            time.sleep(0.5)
            jkdGetCoin()
            jkdAdsCheck()
            driver.find_element_by_id('com.xiangzi.jukandian:id/ll_tab2_layout').click()
            time.sleep(0.5)
            driver.find_element_by_id('com.xiangzi.jukandian:id/ll_tab2_layout').click()
            for i in range(0, watchNewsCount):
                endTime = int(time.time())
                if endTime < (startTime + jkdVideosRunTime * 60):
                    time.sleep(2)
                    #listView = driver.find_element_by_id('com.xiangzi.jukandian:id/view_pager_video')
                    time.sleep(1)
                    videosList = driver.find_elements_by_id('com.xiangzi.jukandian:id/item_video_parent')
                    print(len(videosList))
                    if len(videosList) > 0:
                        videosList[0].click()
                        success = True
                        videosStart = int(time.time())
                        while success:
                            videosEnd = int(time.time())
                            replay = driver.find_elements_by_id('com.xiangzi.jukandian:id/back')
                            if (len(replay) > 0) or (videosEnd > (videosStart + jkdVideosWatch * 60)):
                                # driver.find_element_by_id('cn.weli.story:id/premovie_finish_btn').click()
                                time.sleep(1)
                                success = False
                        driver.back()
                        time.sleep(1)
                        driver.swipe(0, 1100, 0, 300, 500)
                    else:
                        time.sleep(1)
                        driver.swipe(0, 1100, 0, 300, 500)
                else:
                    timeOut = False
                    break
        except Exception or NoSuchElementException:
            print("看视频出现异常，重新启动ing---")
            jkdAdsCheck()
            jkdWindowCheck()
        else:
            break
def qktxWindowCheck():
    # while True:
        ads = driver.find_elements_by_id('com.yanhui.qktx:id/activity_view_groug')
        adsClose = driver.find_elements_by_id('com.yanhui.qktx:id/img_close')
        rootView = driver.find_elements_by_id('com.yanhui.qktx:id/rootView')
        cancle = driver.find_elements_by_id('com.yanhui.qktx:id/bt_open_push_cancle')
        if len(ads) > 0:
            adsClose[0].click()
        elif len(rootView) > 0:
            rootView[0].find_element_by_id('com.yanhui.qktx:id/view_dialog_close').click()
        elif len(cancle) > 0:
            cancle[0].click()
        else:
            # break
            pass
def qktxGetCoin():
    pass
def qukantianxia():
    startTime = int(time.time())
    # while True:
        # try:
    qktxWindowCheck()
    time.sleep(1)
    menuList = driver.find_element_by_id('com.yanhui.qktx:id/main_bottom_bar')
    menu = menuList.find_elements_by_class_name('android.widget.LinearLayout')
    time.sleep(1)
    menu[1].click()

    for i in range(0,watchNewsCount):
        endTime = int(time.time())
        if endTime < (startTime + qktxNewsRunTime * 60):
            news = driver.find_element_by_id('com.yanhui.qktx:id/rv_news')
            newsList = news.find_elements_by_class_name('android.view.ViewGroup')
            time.sleep(1)
            ads = newsList[0].find_elements_by_id('com.yanhui.qktx:id/tv_cursor')
            if len(ads) > 0:
                driver.swipe(0,800,0,220,scrollTime)
            else:
                newsList[0].click()
                time.sleep(2)
                video = driver.find_elements_by_id('com.yanhui.qktx:id/controller_container')
                videoStartTime = int(time.time())
                if len(video) > 0:
                    while True:
                        videoEndTime = int(time.time())
                        replay = driver.find_elements_by_id('com.yanhui.qktx:id/replay')
                        if (videoEndTime > (videoStartTime + qktxVideoTime * 60)) or len(replay) >0:
                            break
                else:
                    webNews = driver.find_elements_by_id('com.yanhui.qktx:id/news_titleView')
                    if len(webNews) > 0:
                        scrollCount = random.randint(startRandom + 5, endRandom + 5)
                        for h in range(0, scrollCount):
                            driver.swipe(0, 400, 0, 220, scrollTime)
                            time.sleep(1.5)
                driver.back()
                driver.swipe(0,800,0,220,scrollTime)
                time.sleep(2)
        # except Exception or NoSuchElementException:
        #     qktxWindowCheck()
        # else:
        #     break

if __name__ == '__main__':
    for a in range(0,runCount):
        for b in range(0,3):
            apk_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
            desired_caps = {}
            desired_caps['platformName'] = 'Android'
            desired_caps['deviceName'] = deviceName #192.168.186.101:5555,cfc4c454
            desired_caps['platformVersion'] = platformVersion
            desired_caps['app'] = apk_path + '\\appium\\apk\\' + appName[b]
            desired_caps['noReset'] = True
            desired_caps['appPackage'] = appPackage[b]
            desired_caps['appActivity'] = appActivity[b]
            driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',desired_caps)
            driver.wait_activity(".base.ui.MainActivity", loadingTime)
            if b == 0: # 微鲤看看
                print("微鲤看看启动，运行----------")
                weiliWatchNews()
                weiliWatchVideos()
                driver.close_app()
                print("微鲤看看关闭++++++++++")
            elif b == 1: # 趣头条
                print("趣头条启动，运行----------")
                qutoutiao()
                driver.close_app()
                print("趣头条关闭++++++++++")
            elif b == 2: # 聚看点
                print("聚看点启动，运行----------")
                jkdWatchNews()
                driver.close_app()
                print("聚看点关闭++++++++++")
                #jkdWatchVideos()
            elif b == 3: # 趣看天下
                print("趣看天下启动，运行----------")
                qukantianxia()
                driver.close_app()
                print("趣看天下关闭++++++++++")
    driver.quit()