CREATE TABLE students (
    id VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    fullname VARCHAR(255) NOT NULL,
    findingGroup BOOLEAN NOT NULL DEFAULT true,
    findingList TEXT[] NOT NULL DEFAULT '{}',
    course TEXT[] NOT NULL DEFAULT '{}',
    authToken VARCHAR(255) NOT NULL,
    saveForumList INT[] NOT NULL DEFAULT '{}'
);

INSERT INTO students (id, password, fullname, findingList, course, authToken, saveForumList) VALUES
    ('63070999', '1234', 'นายสมหมาย เคล็ดขัดยอก', ARRAY['SDTE'], ARRAY['SDTE'], 'test77', '{}'),
    ('63070998', '123', 'นางสาวสมหญิง มิงกะลาบา', ARRAY['SDTE'], ARRAY['SDTE', 'SVV'], 'test556', '{}'),
    ('63070994', '994', 'นางสาวสมสมร นอนหลับไว', '{}', ARRAY['SDTE', 'SVV'], 'test456', '{}'),
    ('63070993', '333', 'นายสมชาย หมายเกรดเอ', ARRAY['CBEAD'], ARRAY['SDTE', 'SVV', 'CBEAD'], 'test226', '{}'),
    ('63070992', '222', 'นายมาโนช มานู่น', ARRAY['CBEAD'], ARRAY['SDTE', 'SVV', 'CBEAD'], 'test536', '{}'),
    ('63070888', '123456', 'นายมาเก๊า โอนไว', '{}', ARRAY['SDTE'], 'test231', '{}'),
    ('63070164', '444', 'นายคิม จองมึน', '{}', ARRAY['SDTE'], 'test225', '{}'),
    ('63070160', '666', 'นายสมอ เท่ห์เสมอ', '{}', ARRAY['SDTE'], 'test335', '{}');

CREATE TABLE pair_students (
    receiver VARCHAR(255) NOT NULL PRIMARY KEY,
    requester VARCHAR(255) NOT NULL,
    course VARCHAR(255) NOT NULL
);

INSERT INTO pair_students (receiver, requester, course) VALUES
    ('63070164', '63070160', 'SDTE');

CREATE TABLE requests (
    id SERIAL PRIMARY KEY,
    receiver VARCHAR(255) NOT NULL,
    requester VARCHAR(255) NOT NULL,
    course VARCHAR(255) NOT NULL
);

INSERT INTO requests (receiver, requester, course) VALUES
    ('63070888', '63070994', 'SDTE'),
    ('63070998', '63070993', 'SDTE'),
    ('63070888', '63070998', 'SDTE'),
    ('63070999', '63070992', 'SDTE');

CREATE TABLE forums (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    imagePath TEXT[] NOT NULL DEFAULT '{}',
    owner VARCHAR(255) NOT NULL,
    anonymous BOOLEAN NOT NULL DEFAULT false,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    course VARCHAR(255) NOT NULL
);

INSERT INTO forums (title, content, imagePath, owner, anonymous, posted_at, course) VALUES
    ('ทำงานอยู่ดีๆโดนแบน AWS ทำไงดีครับ', 'คือผมทำงานอยู่ดีๆแล้ว AWS เด้งแล้วมีเมลส่งมาว่าโดนปิด Account ครับ 😂', ARRAY['awsDeactivation.png'], '63070160', true, CURRENT_TIMESTAMP, 'SDTE'),
    ('ระหว่าง Kubernetes กับ Docker', 'สอบถามครับ ระหว่าง Kubernetes กับ Docker ผมจะเอาสมองส่วนไหนไปจำดีครับ ?', '{}', '63070888', false, CURRENT_TIMESTAMP, 'SDTE');

CREATE TABLE forum_comments (
    id SERIAL PRIMARY KEY,
    forum INT NOT NULL,
    content TEXT NOT NULL,
    owner VARCHAR(255) NOT NULL,
    anonymous BOOLEAN NOT NULL DEFAULT false,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO forum_comments (forum, content, owner, anonymous, posted_at) VALUES
    (1, 'อยากโดนด้วยเลยครับ', '63070164', true, CURRENT_TIMESTAMP);

CREATE TABLE forum_likes (
    forum INT NOT NULL,
    like_from VARCHAR(255) NOT NULL
);

INSERT INTO forum_likes (forum, like_from) VALUES
    (1, '63070164'),
    (1, '63070160'),
    (1, '63070999'),
    (1, '63070998'),
    (1, '63070888'),
    (2, '63070999'),
    (2, '63070998'),
    (2, '63070994'),
    (2, '63070993'),
    (2, '63070992'),
    (2, '63070888'),
    (2, '63070160'),
    (2, '63070164');