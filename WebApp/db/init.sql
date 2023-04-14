CREATE TABLE students (
    id VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    fullname VARCHAR(255) NOT NULL,
    findingGroup BOOLEAN NOT NULL DEFAULT true,
    findingList TEXT[] NOT NULL DEFAULT '{}',
    course TEXT[] NOT NULL DEFAULT '{}',
    authToken VARCHAR(255) NOT NULL,
    forums TEXT[] NOT NULL DEFAULT '{}',
    saveForums TEXT[] NOT NULL DEFAULT '{}'
);

INSERT INTO students (id, password, fullname, findingList, course, authToken, forums, saveForums) VALUES
    ('63070999', '1234', 'นายสมหมาย เคล็ดขัดยอก', ARRAY['SDTE'], ARRAY['SDTE'], 'test77', '{}', '{}'),
    ('63070998', '123', 'นางสาวสมหญิง มิงกะลาบา', ARRAY['SDTE'], ARRAY['SDTE', 'SVV'], 'test456', '{}', '{}'),
    ('63070994', '994', 'นางสาวสมสมร นอนหลับไว', '{}', ARRAY['SDTE', 'SVV'], 'test456', '{}', '{}'),
    ('63070993', '333', 'นายสมชาย หมายเกรดเอ', ARRAY['CBEAD'], ARRAY['SDTE', 'SVV', 'CBEAD'], 'test226', '{}', '{}'),
    ('63070992', '222', 'นายมาโนช มานู่น', ARRAY['CBEAD'], ARRAY['SDTE', 'SVV', 'CBEAD'], 'test536', '{}', '{}'),
    ('63070888', '123456', 'นายมาเก๊า มาไว', '{}', ARRAY['SDTE'], 'test231', '{}', '{}'),
    ('63070164', '444', 'นายคิม จองมึน', '{}', ARRAY['SDTE'], 'test225', '{}', '{}'),
    ('63070160', '666', 'นายสมอ เท่ห์เสมอ', '{}', ARRAY['SDTE'], 'test335', '{}', '{}');

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
    imagePath TEXT[] NOT NULL,
    owner VARCHAR(255) NOT NULL,
    anonymous BOOLEAN NOT NULL DEFAULT false,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    course VARCHAR(255) NOT NULL
);

INSERT INTO forums (title, content, imagePath, owner, anonymous, posted_at, course) VALUES
    ('ทำโปรเจ็คอยู่ดีๆโดนแบน AWS ทำไงดีครับ', 'คือผมทำโปรเจ็คอยู่ดีๆแล้ว AWS เด้งแล้วมีเมลส่งมาว่าโดนปิด Account ครับ', ARRAY['awsDeactivation.png'], '63070160', true, CURRENT_TIMESTAMP, 'SDTE');

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    forum INT NOT NULL,
    content TEXT NOT NULL,
    owner VARCHAR(255) NOT NULL,
    anonymous BOOLEAN NOT NULL DEFAULT false,
    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO comments (forum, content, owner, anonymous, posted_at) VALUES
    (1, 'อยากโดนด้วยเลยครับ', '63070164', true, CURRENT_TIMESTAMP);