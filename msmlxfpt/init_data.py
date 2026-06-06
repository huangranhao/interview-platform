"""初始化题库数据"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Question, JobType, InterviewDifficulty

# 创建数据库连接（与应用程序使用相同的数据库）
engine = create_engine("sqlite:///./interview.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建表
Base.metadata.create_all(bind=engine)

# 初始题目数据
questions_data = [
    # === 技术类 - 初级 ===
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "请解释什么是Python中的装饰器(Decorator)？",
        "answer": "装饰器是Python中一种特殊的函数，它可以用来修改其他函数的行为。装饰器本质上是一个接收函数作为参数并返回一个新函数的函数。装饰器可以在不修改原函数代码的情况下，为函数添加额外的功能，如日志记录、性能测试、权限验证等。",
        "keywords": "Python,装饰器,函数"
    },
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "什么是HTTP状态码？常见的状态码有哪些？",
        "answer": "HTTP状态码是服务器对客户端请求的响应状态的数字代码。常见的状态码包括：200 OK（请求成功）、301 Moved Permanently（永久重定向）、400 Bad Request（请求错误）、401 Unauthorized（未授权）、403 Forbidden（禁止访问）、404 Not Found（资源未找到）、500 Internal Server Error（服务器内部错误）。",
        "keywords": "HTTP,状态码,网络"
    },
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "请解释什么是面向对象编程中的封装、继承和多态？",
        "answer": "封装：将数据和操作数据的方法绑定在一起，对外部隐藏内部实现细节。继承：子类可以继承父类的属性和方法，实现代码复用。多态：同一个接口可以有不同的实现方式，允许不同对象对同一消息做出不同响应。",
        "keywords": "面向对象,封装,继承,多态"
    },
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "什么是RESTful API？它的设计原则是什么？",
        "answer": "RESTful API是一种基于REST架构风格的API设计方式。设计原则包括：使用HTTP方法表示操作（GET获取、POST创建、PUT更新、DELETE删除）、无状态通信、统一接口、资源标识、支持多种数据格式等。",
        "keywords": "REST,API,Web开发"
    },
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "请解释什么是Git版本控制？常用的Git命令有哪些？",
        "answer": "Git是一个分布式版本控制系统，用于跟踪文件的变更历史。常用命令包括：git init（初始化仓库）、git add（暂存文件）、git commit（提交变更）、git push（推送到远程仓库）、git pull（拉取远程更新）、git branch（分支管理）、git merge（合并分支）。",
        "keywords": "Git,版本控制,开发工具"
    },
    
    # === 技术类 - 中级 ===
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "请解释TCP三次握手的过程。",
        "answer": "TCP三次握手是建立TCP连接的过程：1. 客户端发送SYN包给服务器，等待服务器确认；2. 服务器收到SYN包后，发送SYN+ACK包给客户端，表示同意建立连接；3. 客户端收到SYN+ACK包后，发送ACK包给服务器，连接建立完成。三次握手可以防止已失效的连接请求到达服务器，确保双方都具备发送和接收数据的能力。",
        "keywords": "TCP,网络协议,三次握手"
    },
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "什么是数据库索引？为什么需要索引？",
        "answer": "数据库索引是一种数据结构，用于快速查找数据库表中的数据。索引可以类比为书籍的目录，通过索引可以快速定位到需要的数据行，而不需要扫描整个表。索引的主要作用是提高查询性能。但索引也会增加写操作的开销（因为需要维护索引），并占用额外的存储空间。",
        "keywords": "数据库,索引,性能优化"
    },
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "请解释什么是缓存策略？常见的缓存策略有哪些？",
        "answer": "缓存策略是用于管理缓存数据的规则。常见策略包括：LRU（最近最少使用）、LFU（最不经常使用）、FIFO（先进先出）、TTL（时间过期）。缓存可以显著提高系统性能，但需要注意缓存一致性和缓存击穿、雪崩等问题。",
        "keywords": "缓存,性能优化,Redis"
    },
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "什么是线程和进程？它们之间有什么区别？",
        "answer": "进程是操作系统资源分配的基本单位，每个进程有独立的内存空间。线程是CPU调度的基本单位，多个线程共享进程的资源。区别：进程间通信复杂，线程间通信简单；进程开销大，线程开销小；一个进程可以包含多个线程。",
        "keywords": "线程,进程,并发编程"
    },
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "请解释什么是ORM？它的优缺点是什么？",
        "answer": "ORM（对象关系映射）是一种将对象模型和关系数据库映射的技术。优点：提高开发效率、代码更易维护、数据库无关性。缺点：性能开销、复杂查询可能不够灵活、学习成本。常见ORM框架：SQLAlchemy（Python）、Hibernate（Java）、Entity Framework（.NET）。",
        "keywords": "ORM,数据库,SQLAlchemy"
    },
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "什么是跨域问题？如何解决跨域？",
        "answer": "跨域是浏览器的同源策略限制，当请求的协议、域名或端口不同时会触发。解决方案：CORS（后端配置允许跨域）、代理服务器、JSONP（仅支持GET）、WebSocket、Nginx反向代理等。",
        "keywords": "跨域,CORS,前端"
    },
    
    # === 技术类 - 高级 ===
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.SENIOR,
        "content": "请解释什么是微服务架构？它的优缺点是什么？",
        "answer": "微服务架构是一种将应用程序拆分成多个独立、可部署的小型服务的架构风格。每个服务运行在独立的进程中，通过轻量级的通信机制（如HTTP/REST）进行交互。优点：高可扩展性、独立部署、技术多样性、容错性好。缺点：分布式系统复杂性、服务间通信开销、数据一致性问题、运维成本增加。",
        "keywords": "微服务,架构,分布式"
    },
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.SENIOR,
        "content": "如何设计一个高可用的系统？",
        "answer": "设计高可用系统的关键要素：1. 冗余设计：多节点部署、主备切换；2. 负载均衡：分散流量压力；3. 故障隔离：避免单点故障影响全局；4. 自动故障恢复：自动化运维和自愈能力；5. 监控告警：实时监控系统状态；6. 数据备份与恢复：定期备份和灾难恢复计划。",
        "keywords": "高可用,系统设计,架构"
    },
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.SENIOR,
        "content": "请解释CAP定理？在实际应用中如何权衡？",
        "answer": "CAP定理指出分布式系统中，一致性（Consistency）、可用性（Availability）、分区容错性（Partition tolerance）三者不可兼得。实际应用中：需要强一致性场景（如金融交易）选择CP；需要高可用场景（如社交应用）选择AP；大多数互联网系统选择AP，通过最终一致性保证数据一致。",
        "keywords": "CAP定理,分布式,一致性"
    },
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.SENIOR,
        "content": "什么是分布式锁？常见的实现方式有哪些？",
        "answer": "分布式锁是在分布式系统中用于协调多个节点访问共享资源的机制。常见实现方式：1. 基于Redis的SETNX命令；2. 基于ZooKeeper的节点创建；3. 基于数据库的乐观锁/悲观锁。需要考虑锁的过期时间、锁重入、锁释放等问题。",
        "keywords": "分布式锁,Redis,ZooKeeper"
    },
    {
        "job_type": JobType.TECH,
        "difficulty": InterviewDifficulty.SENIOR,
        "content": "请设计一个秒杀系统的架构？",
        "answer": "秒杀系统设计要点：1. 请求削峰：使用消息队列缓冲请求；2. 库存预扣：提前锁定库存；3. 分布式锁：防止超卖；4. 缓存优化：热点数据缓存；5. 限流熔断：保护系统不被压垮；6. 异步处理：下单和支付异步化；7. 数据一致性：最终一致性保证。",
        "keywords": "秒杀系统,高并发,架构设计"
    },
    
    # === 产品类 - 初级 ===
    {
        "job_type": JobType.PRODUCT,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "什么是产品需求文档(PRD)？它包含哪些内容？",
        "answer": "产品需求文档(PRD)是产品经理编写的详细描述产品需求的文档。它通常包含：产品概述、目标用户、功能需求、非功能需求、业务流程、原型设计、数据指标等内容。PRD是开发团队了解需求、进行开发的重要依据。",
        "keywords": "产品需求,PRD,产品文档"
    },
    {
        "job_type": JobType.PRODUCT,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "什么是用户画像？如何构建用户画像？",
        "answer": "用户画像是对目标用户的虚拟代表，包含用户的基本信息、行为特征、需求偏好等。构建步骤：1. 收集用户数据（人口统计、行为数据、调研反馈）；2. 数据清洗和分析；3. 聚类分析分组；4. 定义用户画像标签；5. 输出用户画像文档。",
        "keywords": "用户画像,用户研究,产品"
    },
    {
        "job_type": JobType.PRODUCT,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "什么是MVP？为什么要做MVP？",
        "answer": "MVP（最小可行产品）是指用最少资源实现的、能够验证核心假设的产品版本。做MVP的目的：快速验证市场需求、降低试错成本、尽早获得用户反馈、优化产品方向。MVP不是简单的功能删减，而是保留核心价值的最小集合。",
        "keywords": "MVP,产品开发,创业"
    },
    
    # === 产品类 - 中级 ===
    {
        "job_type": JobType.PRODUCT,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "如何进行用户需求分析？",
        "answer": "用户需求分析的步骤包括：1. 用户调研：通过访谈、问卷等方式收集用户反馈；2. 需求收集：整理用户提出的各种需求；3. 需求分类：将需求分为功能需求和非功能需求；4. 需求优先级排序：使用MoSCoW等方法确定需求优先级；5. 需求验证：与用户确认需求理解是否正确；6. 需求文档编写：输出正式的需求文档。",
        "keywords": "用户需求,需求分析,产品"
    },
    {
        "job_type": JobType.PRODUCT,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "如何进行竞品分析？",
        "answer": "竞品分析步骤：1. 确定竞品范围（直接竞品、间接竞品、潜在竞品）；2. 收集竞品信息（产品功能、用户体验、市场定位、商业模式）；3. 分析竞品优劣势；4. 对比自身产品；5. 提炼差异化机会；6. 输出竞品分析报告。常用方法：SWOT分析、Feature对比矩阵。",
        "keywords": "竞品分析,市场调研,产品策略"
    },
    {
        "job_type": JobType.PRODUCT,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "什么是数据驱动产品？如何用数据驱动产品决策？",
        "answer": "数据驱动产品是指通过数据分析来指导产品决策。方法：1. 建立数据指标体系（核心指标、辅助指标）；2. 数据采集和监控；3. A/B测试验证假设；4. 用户行为分析；5. 数据可视化和报表；6. 定期数据复盘。数据驱动可以减少主观决策，提高决策准确性。",
        "keywords": "数据驱动,数据分析,产品决策"
    },
    {
        "job_type": JobType.PRODUCT,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "如何处理需求变更？",
        "answer": "处理需求变更的方法：1. 建立变更流程：明确变更申请、评估、审批流程；2. 影响评估：评估变更对进度、成本、质量的影响；3. 优先级重新排序：变更需求与原有需求一起重新评估优先级；4. 沟通同步：及时与相关方沟通变更内容；5. 文档更新：更新相关文档记录变更。",
        "keywords": "需求变更,项目管理,产品"
    },
    
    # === 产品类 - 高级 ===
    {
        "job_type": JobType.PRODUCT,
        "difficulty": InterviewDifficulty.SENIOR,
        "content": "如何制定产品路线图？",
        "answer": "制定产品路线图的步骤：1. 明确产品愿景和目标；2. 收集和分析需求；3. 确定优先级（使用RICE、MoSCoW等方法）；4. 划分时间阶段（如季度、半年）；5. 规划各阶段的核心功能和里程碑；6. 与相关方沟通和对齐；7. 定期Review和调整。路线图应该是动态的，需要根据市场变化和用户反馈不断优化。",
        "keywords": "产品路线图,产品规划,战略"
    },
    {
        "job_type": JobType.PRODUCT,
        "difficulty": InterviewDifficulty.SENIOR,
        "content": "如何设计产品的增长策略？",
        "answer": "产品增长策略设计：1. 确定北极星指标；2. 分析增长漏斗（AARRR模型）；3. 识别增长瓶颈；4. 制定增长实验计划；5. 落地执行并监控数据；6. 迭代优化。常见增长手段：病毒式传播、内容营销、用户激励体系、合作伙伴推广等。",
        "keywords": "增长策略,AARRR,产品增长"
    },
    {
        "job_type": JobType.PRODUCT,
        "difficulty": InterviewDifficulty.SENIOR,
        "content": "如何平衡用户体验和商业目标？",
        "answer": "平衡用户体验和商业目标的方法：1. 明确两者的优先级和权衡原则；2. 通过数据量化用户体验和商业指标；3. 寻找双赢方案（如优化转化路径同时提升体验）；4. 用户研究和反馈收集；5. A/B测试验证不同方案的影响；6. 建立跨团队沟通机制，共同决策。",
        "keywords": "用户体验,商业目标,产品策略"
    },
    
    # === 运营类 - 初级 ===
    {
        "job_type": JobType.OPERATION,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "什么是用户运营？主要工作内容有哪些？",
        "answer": "用户运营是通过各种手段提升用户活跃度、留存率和转化率的工作。主要工作内容包括：用户增长（拉新）、用户留存（促活）、用户转化（付费）、用户反馈收集与处理、用户社群运营、活动策划与执行等。",
        "keywords": "用户运营,运营,用户增长"
    },
    {
        "job_type": JobType.OPERATION,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "什么是活动运营？活动运营的流程是什么？",
        "answer": "活动运营是通过策划和执行营销活动来实现特定目标（如拉新、促活、转化）的工作。流程包括：1. 明确活动目标；2. 策划活动方案（主题、形式、规则）；3. 资源协调和准备；4. 活动上线和监控；5. 数据统计和分析；6. 活动复盘总结。",
        "keywords": "活动运营,营销活动,运营"
    },
    {
        "job_type": JobType.OPERATION,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "什么是内容运营？内容运营的核心是什么？",
        "answer": "内容运营是通过创造、编辑、发布和推广内容来吸引和留存用户的工作。核心是：1. 内容策略：明确内容定位和目标；2. 内容创作：产出高质量、有价值的内容；3. 内容分发：选择合适的渠道传播；4. 数据优化：根据数据反馈优化内容策略。",
        "keywords": "内容运营,内容营销,运营"
    },
    
    # === 运营类 - 中级 ===
    {
        "job_type": JobType.OPERATION,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "如何提升用户留存率？",
        "answer": "提升用户留存率的方法：1. 优化用户首次体验（新用户引导）；2. 建立用户激励体系（积分、等级、成就）；3. 个性化推荐和内容推送；4. 用户社群运营（增强归属感）；5. 定期用户反馈收集和产品优化；6. 生命周期管理（针对不同阶段用户采取不同策略）。",
        "keywords": "用户留存,留存率,运营策略"
    },
    {
        "job_type": JobType.OPERATION,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "如何进行用户分层运营？",
        "answer": "用户分层运营步骤：1. 确定分层维度（如活跃度、付费金额、使用频次）；2. 制定分层标准（如RFM模型）；3. 分析各层用户特征和需求；4. 制定差异化运营策略（如高价值用户VIP服务、沉睡用户召回）；5. 执行和监控效果；6. 迭代优化分层策略。",
        "keywords": "用户分层,RFM模型,精细化运营"
    },
    {
        "job_type": JobType.OPERATION,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "如何衡量运营效果？常用的运营指标有哪些？",
        "answer": "衡量运营效果需要建立指标体系：1. 用户增长指标（新增用户、活跃用户、留存率）；2. 转化指标（转化率、客单价、复购率）；3. 内容指标（阅读量、互动率、分享率）；4. 活动指标（参与率、转化率、ROI）。通过数据看板实时监控，定期复盘分析。",
        "keywords": "运营指标,数据分析,效果衡量"
    },
    
    # === 运营类 - 高级 ===
    {
        "job_type": JobType.OPERATION,
        "difficulty": InterviewDifficulty.SENIOR,
        "content": "如何制定用户增长策略？",
        "answer": "用户增长策略制定步骤：1. 明确增长目标和北极星指标；2. 分析用户增长漏斗，识别瓶颈；3. 探索增长渠道（付费渠道、有机增长、病毒传播）；4. 制定获客策略（拉新）、激活策略（首单转化）、留存策略（用户粘性）、变现策略（收入增长）；5. 建立增长实验体系，快速迭代；6. 数据驱动优化。",
        "keywords": "用户增长,增长策略,AARRR"
    },
    {
        "job_type": JobType.OPERATION,
        "difficulty": InterviewDifficulty.SENIOR,
        "content": "如何构建用户激励体系？",
        "answer": "构建用户激励体系：1. 明确激励目标（活跃度、付费、传播）；2. 设计激励机制（积分、等级、勋章、排行榜）；3. 设置激励规则（获取、消耗、过期）；4. 平衡成本和收益；5. 用户分层差异化激励；6. 数据监控和效果评估；7. 迭代优化激励策略。",
        "keywords": "用户激励,积分体系,运营"
    },
    
    # === 设计类 - 初级 ===
    {
        "job_type": JobType.DESIGN,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "什么是UI设计？它与UX设计有什么区别？",
        "answer": "UI设计（用户界面设计）关注的是产品的视觉呈现和交互方式，包括布局、色彩、图标、按钮等元素的设计。UX设计（用户体验设计）关注的是用户使用产品的整体感受和体验，包括用户研究、信息架构、交互设计、可用性测试等。简单来说，UI是产品的外观，UX是产品的使用体验。",
        "keywords": "UI设计,UX设计,设计"
    },
    {
        "job_type": JobType.DESIGN,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "什么是设计规范？为什么需要设计规范？",
        "answer": "设计规范是一套统一的设计标准和准则，包括色彩、字体、间距、组件样式等。设计规范的作用：1. 保证产品视觉一致性；2. 提高设计效率；3. 便于团队协作；4. 降低开发成本；5. 提升品牌形象。",
        "keywords": "设计规范,设计系统,UI"
    },
    {
        "job_type": JobType.DESIGN,
        "difficulty": InterviewDifficulty.JUNIOR,
        "content": "常见的设计工具有哪些？各自的特点是什么？",
        "answer": "常用设计工具：1. Figma：在线协作，适合团队协作；2. Sketch：轻量高效，适合UI设计；3. Adobe XD：集成Adobe生态，适合多平台设计；4. Photoshop：强大的图像处理能力；5. Illustrator：矢量图形设计；6. ProtoPie：交互动效原型。",
        "keywords": "设计工具,Figma,Sketch"
    },
    
    # === 设计类 - 中级 ===
    {
        "job_type": JobType.DESIGN,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "如何进行可用性测试？",
        "answer": "可用性测试步骤：1. 确定测试目标（如发现可用性问题、评估任务完成率）；2. 招募测试用户；3. 设计测试任务；4. 执行测试（观察用户操作、记录问题）；5. 收集反馈；6. 分析数据和问题分类；7. 输出测试报告和改进建议。",
        "keywords": "可用性测试,用户研究,UX"
    },
    {
        "job_type": JobType.DESIGN,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "什么是响应式设计？如何实现响应式设计？",
        "answer": "响应式设计是使网页能够适应不同设备屏幕尺寸的设计方法。实现方式：1. 弹性布局（百分比宽度）；2. 媒体查询（根据屏幕尺寸应用不同样式）；3. 弹性图片和媒体；4. 移动优先设计；5. 使用响应式框架（如Bootstrap）。",
        "keywords": "响应式设计,移动端,前端"
    },
    {
        "job_type": JobType.DESIGN,
        "difficulty": InterviewDifficulty.MIDDLE,
        "content": "如何设计一套品牌视觉系统？",
        "answer": "品牌视觉系统设计步骤：1. 品牌定位和核心价值分析；2. Logo设计（图形、字体、颜色）；3. 色彩系统（主色、辅助色、中性色）；4. 字体系统（标题、正文、辅助文字）；5. 图形元素和图标；6. 应用规范（名片、海报、网站等）；7. 输出品牌手册。",
        "keywords": "品牌设计,视觉系统,VI"
    },
    
    # === 设计类 - 高级 ===
    {
        "job_type": JobType.DESIGN,
        "difficulty": InterviewDifficulty.SENIOR,
        "content": "如何构建设计系统？",
        "answer": "构建设计系统步骤：1. 规划设计系统范围（组件库、设计规范、工具链）；2. 建立设计语言（色彩、字体、间距、图标）；3. 设计组件库（按钮、输入框、卡片等）；4. 开发组件代码；5. 建立文档和协作流程；6. 持续维护和迭代。设计系统可以提高设计和开发效率，保证产品一致性。",
        "keywords": "设计系统,组件库,Design System"
    },
    {
        "job_type": JobType.DESIGN,
        "difficulty": InterviewDifficulty.SENIOR,
        "content": "如何进行设计决策的量化评估？",
        "answer": "设计决策量化评估方法：1. 建立评估指标体系（可用性、效率、满意度）；2. A/B测试对比不同设计方案；3. 用户测试收集定性和定量数据；4. 数据分析（任务完成率、错误率、时间花费）；5. 用户满意度调研（NPS、CSAT）；6. 数据可视化和报告输出。",
        "keywords": "设计评估,A/B测试,数据驱动"
    }
]

def init_questions():
    db = SessionLocal()
    
    # 清空现有数据
    db.query(Question).delete()
    db.commit()
    print("已清空现有题目")
    
    # 添加初始题目
    for q_data in questions_data:
        question = Question(**q_data)
        db.add(question)
    
    db.commit()
    print(f"成功添加 {len(questions_data)} 道题目")
    
    db.close()

if __name__ == "__main__":
    init_questions()
