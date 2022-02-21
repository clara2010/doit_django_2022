from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        self.assertEqual(2, 2)

        # 1.1 포스트 목록 페이지(Post list)를 연다.
        response = self.client.get('/blog/')

        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)

        # 1.3 페이지의 타이틀에 blog라는 문구가 있다,
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn('Blog', soup.title.text)

        # 1.4 NavBar가 있다.
        navbar = soup.nav

        # 1.5 Blog, About Me라는 문구가 네비게이션 바에 있다.
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)


        # 2.1 메인 영역에 게시물이 하나도 없다면
        # 2.1 @실제 블로그 Post 갯수와 무관하게 장고에서 test용 DB를 만들어서 테스트!-> Post 수 0
        self.assertEqual(Post.objects.count(),0)

        # 2.2 메인 영역에 "아직 게시물이 없습니다."라는 문구가 나온다.
        main_area = soup.find('div', id='main-area')
        self.assertIn("아직 게시물이 없습니다", main_area.text)

        # 3.1 만약 게시물이 2개 있다면,
        # 2.1@이기 때문에 포스트를 만들어 줘야 한다.
        post_001 = Post.objects.create(
            title = '첫 번째 포스트 입니다',
            content = 'Hello World, We are the world'
        )
        post_002 = Post.objects.create(
            title = '두 번째 포스트 입니다',
            content = '1등이 전부는 아니잖아요'
        )

        self.assertEqual(Post.objects.count(),2)

        # 3.2 포스트 목록 페이지를 새로 고침했을 때,
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        # 3.4 "아직 게시물이 없습니다"라는 문구가 없어야 한다.
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)
