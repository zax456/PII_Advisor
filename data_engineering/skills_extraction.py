import re

with open('./skills.txt', 'rb') as f:
    skills = f.readlines()

skills = [skill.decode('utf8').strip().lower() for skill in skills]
skills_multi_word = [skill for skill in skills if len(skill.split(' ')) > 1]
skills_single_word = [skill for skill in skills if len(skill.split(' ')) == 1]

ddir = '../../../../data/resumes/batch1' # path to resumes
for resume_num in [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]:
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
    ddir = '.' # output folder
    with open(f'{ddir}/extracted_skills_by_resume.csv', 'a') as f: # append to the file since this is a for loop
        f.write(f'{resume_num},{",".join(identified_skills)}')
