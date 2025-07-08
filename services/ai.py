# services/ai.py

import openai
import google.generativeai as genai
from core import settings
import copy

openai.api_key = settings.OPENAI_API_KEY
genai.configure(api_key=settings.GENAI_API_KEY)

class OpenAIClient():

    def __init__(self):
        self.model = settings.OPENAI_EMBEDDING_MODEL
        self.dim = settings.OPENAI_EMBEDDING_DIM

    def get_embedding(self, text):
        response = openai.Embedding.create(
            input=text,
            model=self.model,
            dimensions=self.dim
        )
        print("OpenAI : make embedding")
        return response["data"][0]["embedding"]
    
class GenAIClient():

    def __init__(self):
        self.model = settings.GENAI_MODEL

    def _concatenate_abstracts(self, papers):
        abstracts = [paper.abstract for paper in papers]
        combined_text = "\n\n".join(abstracts)
        return combined_text

    def translate_abstract(self, papers):
        print(f"GenAI : Trying to translate {len(papers)} papers...", end=" ")
        text = self._concatenate_abstracts(papers)
        model = genai.GenerativeModel(self.model)
        prompt = f"""## 역할, 목표

당신은 유능한 콘텐츠 번역가입니다.
[제공 자료] 를 누락 없이 완전히 번역하세요.

## 번역 원칙

1. 완전성 : 원문의 모든 내용을 빠짐없이 번역하세요.
2. 정확성 : 원문의 의미와 뉘앙스를 정확히 전달하세요.
3. 자연스러움 : 한국어로 자연스럽게 읽히도록 번역하세요.
4. 분리성 : 문단과 문단 간 내용이 섞이지 않도록 분리하세요.

## 톤

’Spartan tone’ 을 사용합니다.

## 출력 형식

- 번역된 내용만 출력해 주세요.
- 입력과 동일한 방식으로 문단을 나누어 가독성을 높이세요.
- 문단 사이는 입력과 동일하게 \n\n 로 구분하세요.

## 제공 자료

<제공 자료>
{text}
</제공 자료>

## 주의사항
- 전문 용어는 적절한 한국어로 번역하되, 필요시 원문을 () 안에 병기하세요.
- 고유명사는 한국어 표기법을 따르세요.
- 내용 추가나 삭제 없이 원문의 모든 정보를 포함하세요.
"""
        response = model.generate_content(prompt)
        translated_abstracts = response.text.strip().split("\n\n")
        translated_papers = []
        for p, abstract in zip(papers, translated_abstracts):
            new_p = copy.deepcopy(p)
            new_p.abstract = abstract
            translated_papers.append(new_p)
        print(f"OK, {len(translated_papers)} papers translated.")
        return translated_papers