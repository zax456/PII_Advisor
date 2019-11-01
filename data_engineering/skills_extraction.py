import re

with open('./skills.txt', 'rb') as f:
    skills = f.readlines()

skills = [skill.decode('utf8').strip().lower() for skill in skills]
skills_multi_word = [skill for skill in skills if len(skill.split(' ')) > 1]
skills_single_word = [skill for skill in skills if len(skill.split(' ')) == 1]

ddir = '../../../../data/resumes/batch4' # path to resumes
for resume_num in [1524, 1522, 1521, 1520, 1519, 1518, 1517, 1516, 1515, 1514, 1513, 1512, 1511, 1510, 1509, 1508, 1506, 1505, 1504, 1503, 1502, 1501, 1500, 1499, 1498, 1497, 1496, 1495, 1494, 1492]:
    with open(f'{ddir}/resume number {resume_num}.txt', encoding='utf8' , errors='ignore') as f:
        resume_text = f.readlines()

    resume_text = [line.strip().lower() for line in resume_text]

    identified_skills = set()

    # to identify multi-worded skills
    for skill in skills_multi_word:
        for i, line in enumerate(resume_text):
            if skill in line:
                identified_skills.add(skill)
                resume_text[i] = re.sub(skill, '<skill_extracted>', line)

    # to identify single-worded skills
    # start by breaking resume text into single words
    resume_words = set()
    for line in resume_text:
        for word in line.strip().split(' '):
            resume_words.add(word)

    for skill in skills_single_word:
        if skill in resume_words:
            identified_skills.add(skill)

    # output results
    with open('./extracted_skills_by_resume.csv', 'a') as f: # append to the file since this is a for loop
        f.write(f'{resume_num},{",".join(identified_skills)}\n')
