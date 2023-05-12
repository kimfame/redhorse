import random

LOREM_IPSUM_WORDS = "lorem ipsum lacus elit ex maximus inceptos auctor sit vestibulum integer eget non velit nulla quis ipsum tincidunt interdum adipiscing porttitor risus arcu mi magna facilisis fermentum congue ad dolor placerat dolore augue ipsum morbi lobortis ac a aenean justo eu ut rutrum tempor vulputate eu exercitation metus taciti veniam id nullam occaecat vel consectetur suscipit vulputate urna varius mus aptent faucibus ex ex vel rhoncus aute non eiusmod quisque commodo ut magnis aliquet egestas hendrerit minim eget neque nibh luctus in nisi sapien conubia mattis augue magna quam qui id morbi cillum lacus sunt in vulputate cras sagittis lacinia odio massa et metus ultricies mollis nibh torquent iaculis erat proident orci sapien sagittis vulputate et aliquip eget deserunt sapien habitasse non vitae augue egestas varius dolor sit lacinia proin eget fringilla nunc lectus dui ea duis lectus pulvinar placerat eu massa orci orci curabitur nec eu enim dolor nunc ac sed arcu varius leo vitae tellus bibendum nisi culpa justo ut nisl class sint donec erat et orci fringilla sit nibh libero ultricies ultricies incididunt vulputate consequat enim facilisis auctor penatibus dolor at nec mauris sed quam interdum mattis in vel et id tempus suscipit nisi luctus quis neque sed imperdiet porta sociosqu donec volutpat vitae imperdiet ligula sit ut volutpat dictumst quis tortor arcu amet ut erat proin sed consectetur himenaeos irure luctus proin magna cupidatat justo hac tristique felis ullamcorper accumsan in lacinia eleifend in fusce porta et ligula neque donec consequat platea placerat a tincidunt do id fringilla nibh quis tempus officia fringilla aliqua a ac esse venenatis labore lorem turpis eu pellentesque tincidunt dui eros ultricies elit nibh laboris quis suscipit sed eleifend placerat odio maximus vitae posuere morbi tristique tempor commodo nisl eget sed ridiculus at dictum dui amet sed non parturient volutpat convallis scelerisque porttitor ut est maximus lobortis augue cras in molestie amet erat nisi non turpis tincidunt enim urna dignissim pretium mollit nulla excepteur in hendrerit orci massa est natoque laborum nisi sem quis eget integer diam ad volutpat suscipit per ut fugiat et a quisque eget vehicula ante at quam arcu nam donec velit gravida in vitae ultricies maecenas ac non reprehenderit sed vehicula vehicula finibus ut vulputate curabitur posuere sem sapien felis interdum ut amet praesent felis fermentum duis convallis sodales nisi dis montes lectus consequat phasellus pariatur porttitor nostrud eleifend sed nostra volutpat vel metus cursus metus nunc ex arcu velit aliquam molestie dolore et leo et per nulla mauris proin quam eu tincidunt massa nisl eros suscipit sed quis ultricies integer quis litora nascetur voluptate massa ut ullamco est anim volutpat pulvinar tempus".split()


def get_one_sentence():
    return " ".join(random.sample(LOREM_IPSUM_WORDS, random.randint(4, 12)))


def get_one_paragraph(max_length=500, sentence_range=(4, 15)):
    paragraph = ""

    for _ in range(random.randint(*sentence_range)):
        sentence = get_one_sentence()

        if max_length > len(paragraph + sentence) + 2:
            if len(paragraph) == 0:
                paragraph = sentence
            else:
                paragraph += f"{random.choice('.,')} {sentence}"
        else:
            break

    return f"{paragraph[0].upper()}{paragraph[1:]}."
