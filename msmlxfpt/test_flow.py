import requests

# 基础URL
BASE_URL = 'http://127.0.0.1:8888'

print('='*60)
print('步骤1: 用户注册')
print('='*60)

# 注册新用户
register_data = {
    'phone': '13800138002',
    'password': 'test123456',
    'nickname': '测试用户'
}
try:
    response = requests.post(f'{BASE_URL}/api/auth/register', json=register_data)
    print(f'注册状态: {response.status_code}')
    print(f'响应头: {response.headers}')
    print(f'响应内容: {response.text[:500]}')
    if response.status_code == 200:
        print(f'注册响应: {response.json()}')
except Exception as e:
    print(f'请求异常: {e}')

print()
print('='*60)
print('步骤2: 用户登录获取JWT令牌')
print('='*60)

# 用户登录（使用已存在的测试用户）
login_data = {
    'username': '13800138001',
    'password': 'user123'
}
try:
    response = requests.post(f'{BASE_URL}/api/auth/login', data=login_data)
    print(f'登录状态: {response.status_code}')
    print(f'响应内容: {response.text[:500]}')
    if response.status_code == 200:
        result = response.json()
        print(f'登录响应: {result}')
        token = result.get('access_token')
        headers = {'Authorization': f'Bearer {token}'}
        
        print()
        print('='*60)
        print('步骤3: 访问题库')
        print('='*60)

        # 获取题库列表
        response = requests.get(f'{BASE_URL}/api/questions/', headers=headers)
        print(f'题库状态: {response.status_code}')
        questions = response.json()
        print(f'题目数量: {len(questions)}')
        print(f'第一个题目: {questions[0]}')

        print()
        print('='*60)
        print('步骤4: 收藏题目')
        print('='*60)

        # 收藏第一个题目
        question_id = questions[0]['id']
        response = requests.post(f'{BASE_URL}/api/questions/{question_id}/favorite', headers=headers)
        print(f'收藏状态: {response.status_code}')
        print(f'收藏响应: {response.json()}')

        print()
        print('='*60)
        print('步骤5: 开始面试')
        print('='*60)

        # 开始面试
        start_data = {
            'job_type': 'tech',
            'difficulty': 'junior',
            'duration': 300
        }
        response = requests.post(f'{BASE_URL}/api/interview/start', json=start_data, headers=headers)
        print(f'开始面试状态: {response.status_code}')
        interview = response.json()
        print(f'面试信息: {interview}')
        interview_id = interview['id']

        print()
        print('='*60)
        print('步骤6: 获取面试题目并回答')
        print('='*60)

        # 获取面试题目
        response = requests.get(f'{BASE_URL}/api/interview/{interview_id}/questions', headers=headers)
        print(f'获取题目状态: {response.status_code}')
        interview_questions = response.json()
        print(f'面试题目数量: {len(interview_questions)}')

        # 回答第一个问题（使用查询参数）
        if interview_questions:
            params = {
                'question_id': interview_questions[0]['id'],  # 注意这里应该是interview_question的id，不是question_id
                'answer': '我认为Python是一种非常优秀的编程语言，它具有简洁的语法和强大的生态系统。',
                'answer_time': 60
            }
            response = requests.post(f'{BASE_URL}/api/interview/{interview_id}/answer', params=params, headers=headers)
            print(f'回答状态: {response.status_code}')
            print(f'回答响应: {response.json()}')

        print()
        print('='*60)
        print('步骤7: 完成面试')
        print('='*60)

        # 完成面试
        response = requests.post(f'{BASE_URL}/api/interview/{interview_id}/complete', headers=headers)
        print(f'完成面试状态: {response.status_code}')
        print(f'完成响应: {response.json()}')

        print()
        print('='*60)
        print('步骤8: 生成并查看AI评估报告')
        print('='*60)

        # 生成评估报告
        response = requests.post(f'{BASE_URL}/api/assessment/{interview_id}', headers=headers)
        print(f'生成报告状态: {response.status_code}')
        if response.status_code == 200:
            print(f'生成响应: {response.json()}')
            
            # 获取评估报告
            response = requests.get(f'{BASE_URL}/api/assessment/{interview_id}', headers=headers)
            print(f'评估报告状态: {response.status_code}')
            assessment = response.json()
            print(f'评估报告: {assessment}')

        print()
        print('='*60)
        print('步骤9: 学习中心')
        print('='*60)

        # 获取学习资源
        response = requests.get(f'{BASE_URL}/api/learning/resources', headers=headers)
        print(f'学习资源状态: {response.status_code}')
        resources = response.json()
        print(f'学习资源数量: {len(resources)}')
        print(f'第一个资源: {resources[0]}')

        print()
        print('='*60)
        print('所有流程测试完成！')
        print('='*60)
except Exception as e:
    print(f'请求异常: {e}')
