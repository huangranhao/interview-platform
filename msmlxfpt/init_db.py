"""数据库初始化脚本"""
from app.database import engine, Base
from app.models import User, Question, LearningResource, JobType, InterviewDifficulty
from app.utils import get_password_hash, generate_nickname

# 创建所有表
Base.metadata.create_all(bind=engine)

# 插入测试数据
def insert_test_data():
    from app.database import SessionLocal
    
    db = SessionLocal()
    
    try:
        # 检查是否已存在测试数据
        if db.query(User).first():
            print("测试数据已存在，跳过插入")
            return
        
        # 创建管理员用户
        admin_user = User(
            phone="13800138000",
            email="admin@example.com",
            password_hash=get_password_hash("admin123"),
            nickname="管理员",
            role="admin"
        )
        db.add(admin_user)
        
        # 创建测试用户
        test_user = User(
            phone="13800138001",
            email="user@example.com",
            password_hash=get_password_hash("user123"),
            nickname=generate_nickname(),
            role="user"
        )
        db.add(test_user)
        
        # 插入测试题目
        test_questions = [
            {
                "job_type": "tech",
                "difficulty": "junior",
                "content": "请介绍一下Python中的装饰器是什么？",
                "answer": "装饰器是一种特殊类型的函数，可以用来修改或增强其他函数的功能。装饰器在不修改原函数代码的情况下，为函数添加额外的功能。",
                "keywords": "装饰器,函数,增强"
            },
            {
                "job_type": "tech",
                "difficulty": "junior",
                "content": "什么是面向对象编程？",
                "answer": "面向对象编程是一种编程范式，它以对象为基本单元，将数据和操作数据的方法封装在一起。主要特征包括封装、继承和多态。",
                "keywords": "面向对象,封装,继承,多态"
            },
            {
                "job_type": "tech",
                "difficulty": "middle",
                "content": "请解释什么是RESTful API？",
                "answer": "RESTful API是一种基于REST架构风格的Web服务设计方式，使用HTTP方法（GET、POST、PUT、DELETE）进行资源操作，具有无状态、统一接口等特点。",
                "keywords": "REST,API,HTTP,资源"
            },
            {
                "job_type": "tech",
                "difficulty": "middle",
                "content": "什么是微服务架构？它有什么优缺点？",
                "answer": "微服务架构是一种将应用程序拆分为一组小型、独立服务的架构风格。优点包括高可扩展性、独立部署、技术多样性；缺点包括分布式系统复杂性、服务间通信开销。",
                "keywords": "微服务,架构,分布式,服务"
            },
            {
                "job_type": "tech",
                "difficulty": "senior",
                "content": "请设计一个高并发系统的架构方案",
                "answer": "高并发系统设计需要考虑：负载均衡、缓存策略、数据库读写分离、消息队列解耦、分布式锁、限流熔断等。常用架构包括分层架构、事件驱动架构等。",
                "keywords": "高并发,负载均衡,缓存,分布式"
            },
            {
                "job_type": "product",
                "difficulty": "junior",
                "content": "什么是产品需求文档（PRD）？",
                "answer": "产品需求文档是产品经理编写的详细说明文档，包含产品目标、功能需求、非功能需求、用户故事、原型设计等内容，是开发团队的重要参考依据。",
                "keywords": "PRD,需求文档,产品经理"
            },
            {
                "job_type": "product",
                "difficulty": "middle",
                "content": "如何进行用户需求分析？",
                "answer": "用户需求分析方法包括：用户调研、竞品分析、数据分析、用户访谈、可用性测试等。核心是理解用户痛点和真实需求，将其转化为产品功能。",
                "keywords": "需求分析,用户调研,竞品分析"
            },
            {
                "job_type": "operation",
                "difficulty": "junior",
                "content": "什么是用户运营？",
                "answer": "用户运营是通过各种手段提升用户活跃度、留存率和转化率的工作，包括用户拉新、用户激活、用户留存、用户变现等环节。",
                "keywords": "用户运营,活跃度,留存率"
            },
            {
                "job_type": "operation",
                "difficulty": "middle",
                "content": "如何制定运营策略？",
                "answer": "运营策略制定需要：明确目标、分析用户、选择渠道、设计活动、数据监测、效果评估。关键是基于数据驱动的持续优化。",
                "keywords": "运营策略,数据驱动,用户分析"
            },
            {
                "job_type": "design",
                "difficulty": "junior",
                "content": "什么是UI设计和UX设计？",
                "answer": "UI设计关注界面的视觉呈现，包括布局、色彩、字体等；UX设计关注用户体验，包括可用性、易用性、用户满意度等。两者相辅相成，共同提升产品体验。",
                "keywords": "UI,UX,用户体验,界面设计"
            }
        ]
        
        for q in test_questions:
            question = Question(
                job_type=JobType(q["job_type"]),
                difficulty=InterviewDifficulty(q["difficulty"]),
                content=q["content"],
                answer=q["answer"],
                keywords=q["keywords"]
            )
            db.add(question)
        
        # 插入学习资源
        learning_resources = [
            {
                "title": "Python面试技巧",
                "content": "## Python面试技巧\n\n### 1. 基础知识准备\n- 熟悉Python基础语法\n- 理解面向对象编程\n- 掌握常用数据结构\n\n### 2. 常见问题\n- 装饰器的使用\n- 生成器和迭代器\n- 异常处理机制\n\n### 3. 实战建议\n- 多做练习题\n- 模拟面试练习\n- 总结面试经验",
                "resource_type": "article",
                "job_type": "tech",
                "difficulty": "junior"
            },
            {
                "title": "产品经理面试指南",
                "content": "## 产品经理面试指南\n\n### 1. 简历准备\n- 突出项目经验\n- 量化成果\n- 展示产品思维\n\n### 2. 面试技巧\n- 清晰表达想法\n- 结构化回答问题\n- 展示产品sense\n\n### 3. 常见问题\n- 为什么选择产品经理\n- 做过最成功的产品\n- 如何处理需求冲突",
                "resource_type": "article",
                "job_type": "product",
                "difficulty": "middle"
            },
            {
                "title": "运营岗位面试准备",
                "content": "## 运营岗位面试准备\n\n### 1. 了解岗位\n- 用户运营 vs 内容运营\n- 活动运营 vs 数据运营\n\n### 2. 技能准备\n- 数据分析能力\n- 文案写作能力\n- 活动策划能力\n\n### 3. 面试要点\n- 过往项目经验\n- 数据驱动思维\n- 创新能力",
                "resource_type": "article",
                "job_type": "operation",
                "difficulty": "junior"
            }
        ]
        
        for lr in learning_resources:
            resource = LearningResource(
                title=lr["title"],
                content=lr["content"],
                resource_type=lr["resource_type"],
                job_type=JobType(lr["job_type"]),
                difficulty=InterviewDifficulty(lr["difficulty"])
            )
            db.add(resource)
        
        db.commit()
        print("测试数据插入成功")
        
    except Exception as e:
        db.rollback()
        print(f"插入测试数据失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    insert_test_data()
