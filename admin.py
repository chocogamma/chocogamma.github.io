import markdown2
import json
import sys
import ast
import os

draft = '''--------------------------------------------------------------------------------
title : Undefined
tags  : ["undefined"]
--------------------------------------------------------------------------------
'''

htmlBefore = '''<!DOCTYPE html>
<html lang="zh-Hant">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="black">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <title>PageTitle</title>
    <link rel="shortcut icon" href="/favicon.ico">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="/css/main.min.css">
  </head>
  <body>
    <header class="bg-dark sticky-top">
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark container">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <span class="d-lg-none percentage-text text-warning">100 %</span>
        <a class="navbar-brand" href="/"><img src="/apple-touch-icon.png" alt="brand" width="36"></a>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <a class="nav-link" href="/">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/page/tags.html">Tags</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/page/about.html">About</a>
            </li>
          </ul>
          <ul class="navbar-nav mr-auto d-none d-lg-block">
            <li class="nav-item">
              <a class="nav-link disabled percentage-text text-warning" href="#" tabindex="-1" aria-disabled="true">100 %</a>
            </li>
          </ul>
          <form class="form-inline d-inline-block">
            <input id="inputs" class="form-control mr-sm-2" type="search" placeholder="Search Title" aria-label="Search">
          </form>
          <button id="search" class="btn btn-outline-warning ml-2 ml-md-0 my-2 my-sm-0 d-inline-block" type="button">Search</button>
        </div>
      </nav>
      <section class="percentage-bar bg-warning"></section>
    </header>
'''

htmlAbout = '''<!DOCTYPE html>
<html lang="zh-Hant">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="black">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <title>About - Gold Dolphin</title>
    <link rel="shortcut icon" href="/favicon.ico">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="/css/main.min.css">
  </head>
  <body>
    <header class="bg-dark sticky-top">
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark container">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <span class="d-lg-none percentage-text text-warning">100 %</span>
        <a class="navbar-brand" href="/"><img src="/apple-touch-icon.png" alt="brand" width="36"></a>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <a class="nav-link" href="/">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/page/tags.html">Tags</a>
            </li>
            <li class="nav-item active">
              <a class="nav-link" href="/page/about.html">About <span class="sr-only">(current)</span></a>
            </li>
          </ul>
          <ul class="navbar-nav mr-auto d-none d-lg-block">
            <li class="nav-item">
              <a class="nav-link disabled percentage-text text-warning" href="#" tabindex="-1" aria-disabled="true">100 %</a>
            </li>
          </ul>
          <form class="form-inline d-inline-block">
            <input id="inputs" class="form-control mr-sm-2" type="search" placeholder="Search Title" aria-label="Search">
          </form>
          <button id="search" class="btn btn-outline-warning ml-2 ml-md-0 my-2 my-sm-0 d-inline-block" type="button">Search</button>
        </div>
      </nav>
      <section class="percentage-bar bg-warning"></section>
    </header>
'''

htmlAfter = '''    <main class="mt-1 my-md-5">
      <article class="container shadow mb-1 mb-md-5">
        PageArticle
      </article>
    </main>

    <div class="toggle-top rounded-circle"><img src="/img/top-menu.png" alt="top-menu"></div>

    <!-- Bootstrap -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
    <script src="/js/navbar.js"></script>
    <script src="/js/search.js"></script>
    <script src="/js/toggle.js"></script>
    <script src="/js/prism.js"></script>
  </body>
</html>
'''

def new_draft(file):
    if os.path.isfile('./article/post/{}.md'.format(file)):
        print('Warning: {}.md 檔案已存在!'.format(file))

    else:
        with open('./article/post/{}.md'.format(file), 'w', encoding='utf-8') as f:
            f.write(draft)
        print('Success: 已建立 {}.md 檔案!'.format(file))


def add_article(file):
    if not os.path.isfile('./article/post/{}.md'.format(file)):
        print('Warning: {}.md 檔案不存在!'.format(file))

    elif os.path.isfile('./post/{}.html'.format(file)):
        print('Warning: {}.html 檔案已存在!'.format(file))

    else:
        with open('./article/post/{}.md'.format(file), 'r', encoding='utf-8') as f:
            preText = f.readlines()
            for line in range(len(preText)):
                if preText[line] == '```html\n':
                    index = line
                    while preText[index + 1] != '```\n':
                        index += 1
                        preText[index] = '    ' + preText[index]

        with open('./article/post/{}.md'.format(file), 'w', encoding='utf-8') as f:
            for line in preText:
                f.write(line)

        with open('./article/post/{}.md'.format(file), 'r', encoding='utf-8') as f:
            f.readline()
            title = f.readline().lstrip('title ').lstrip(':').strip()
            tags = ast.literal_eval(f.readline().lstrip('tags ').lstrip(':').strip())
            f.readline()
            text = f.read()
            html = markdown2.markdown(text).split('\n')

        for line in range(len(html)):
            if html[line].startswith('<p><code>'):
                language = html[line].split('<p><code>')[1].strip()
                html[line] = '<pre><code class="language-{} line-numbers">'.format(language)

            if html[line].endswith('</code></p>'):
                html[line] = '</code></pre>'

            if html[line].startswith('<p><img') and html[line].endswith('></p>'):
                c1 = html[line].find('"', 0)
                c2 = html[line].find('"', c1 + 1)
                c3 = html[line].find('"', c2 + 1)
                c4 = html[line].find('"', c3 + 1)
                html[line] = '<figure>' + \
                             '<img src="{}" alt="{}">'.format(html[line][c1+1:c2], html[line][c3+1:c4]) + \
                             '<figcaption>{}</figcaption>'.format(html[line][c3+1:c4]) + \
                             '</figure>'

        for line in range(len(html)):
            if html[line] == '<pre><code class="language-html line-numbers">':
                index = line
                while html[index + 1] != '</code></pre>':
                    index += 1
                    html[index] = html[index][4:]

        index = 0
        while index < len(html):
            if not (html[index].startswith('<pre><code class="language-') and html[index].endswith('line-numbers">')):
                index +=1
            else:
                html[index] += html[index + 1]
                del html[index + 1]

        html = '\n'.join(html)
        html = htmlBefore.replace('PageTitle', title + ' - Gold Dolphin') + htmlAfter.replace('PageArticle', html)

        with open('./post/{}.html'.format(file), 'w', encoding='utf-8') as f:
            f.write(html)

        with open('./article/post/{}.md'.format(file), 'r', encoding='utf-8') as f:
            preText = f.readlines()
            for line in range(len(preText)):
                if preText[line] == '```html\n':
                    index = line
                    while preText[index + 1] != '```\n':
                        index += 1
                        preText[index] = preText[index][4:]

        with open('./article/post/{}.md'.format(file), 'w', encoding='utf-8') as f:
            for line in preText:
                f.write(line)

        with open('./js/posturl.json', 'r', encoding='utf-8') as f:
            jsonData = json.load(f)

        newData = {file + '.html': {'title': title, 'tags': tags}}
        newData.update(jsonData)
        jsonData = newData.copy()

        with open('./js/posturl.json', 'w', encoding='utf-8') as f:
            json.dump(jsonData, f)

        print('Success: 已建立 {}.html 檔案!'.format(file))


def update_article(file):
    if not os.path.isfile('./article/post/{}.md'.format(file)):
        print('Warning: {}.md 檔案不存在!'.format(file))

    else:
        answer = input('是否要執行檔案更新 (N/y): ')
        if not (answer == 'Y' or answer == 'y'):
            print('Warning: 選擇不更新!')

        else:
            with open('./article/post/{}.md'.format(file), 'r', encoding='utf-8') as f:
                preText = f.readlines()
                for line in range(len(preText)):
                    if preText[line] == '```html\n':
                        index = line
                        while preText[index + 1] != '```\n':
                            index += 1
                            preText[index] = '    ' + preText[index]

            with open('./article/post/{}.md'.format(file), 'w', encoding='utf-8') as f:
                for line in preText:
                    f.write(line)

            with open('./article/post/{}.md'.format(file), 'r', encoding='utf-8') as f:
                f.readline()
                title = f.readline().lstrip('title ').lstrip(':').strip()
                tags = ast.literal_eval(f.readline().lstrip('tags ').lstrip(':').strip())
                f.readline()
                text = f.read()
                html = markdown2.markdown(text).split('\n')

            for line in range(len(html)):
                if html[line].startswith('<p><code>'):
                    language = html[line].split('<p><code>')[1].strip()
                    html[line] = '<pre><code class="language-{} line-numbers">'.format(language)

                if html[line].endswith('</code></p>'):
                    html[line] = '</code></pre>'

                if html[line].startswith('<p><img') and html[line].endswith('></p>'):
                    c1 = html[line].find('"', 0)
                    c2 = html[line].find('"', c1 + 1)
                    c3 = html[line].find('"', c2 + 1)
                    c4 = html[line].find('"', c3 + 1)
                    html[line] = '<figure>' + \
                                 '<img src="{}" alt="{}">'.format(html[line][c1+1:c2], html[line][c3+1:c4]) + \
                                 '<figcaption>{}</figcaption>'.format(html[line][c3+1:c4]) + \
                                 '</figure>'

            for line in range(len(html)):
                if html[line] == '<pre><code class="language-html line-numbers">':
                    index = line
                    while html[index + 1] != '</code></pre>':
                        index += 1
                        html[index] = html[index][4:]

            index = 0
            while index < len(html):
                if not (html[index].startswith('<pre><code class="language-') and html[index].endswith('line-numbers">')):
                    index +=1
                else:
                    html[index] += html[index + 1]
                    del html[index + 1]

            html = '\n'.join(html)
            html = htmlBefore.replace('PageTitle', title + ' - Gold Dolphin') + htmlAfter.replace('PageArticle', html)

            with open('./post/{}.html'.format(file), 'w', encoding='utf-8') as f:
                f.write(html)

            with open('./article/post/{}.md'.format(file), 'r', encoding='utf-8') as f:
                preText = f.readlines()
                for line in range(len(preText)):
                    if preText[line] == '```html\n':
                        index = line
                        while preText[index + 1] != '```\n':
                            index += 1
                            preText[index] = preText[index][4:]

            with open('./article/post/{}.md'.format(file), 'w', encoding='utf-8') as f:
                for line in preText:
                    f.write(line)

            with open('./js/posturl.json', 'r', encoding='utf-8') as f:
                jsonData = json.load(f)

            answer2 = input('是否將文章順序移到最前面 (N/y): ')
            if not (answer2 == 'Y' or answer2 == 'y'):
                jsonData[file + '.html']['title'] = title
                jsonData[file + '.html']['tags'] = tags

                with open('./js/posturl.json', 'w', encoding='utf-8') as f:
                    json.dump(jsonData, f)
                print('Success: 更新成功! (文章順序未變更)')

            else:
                del jsonData[file + '.html']
                newData = {file + '.html': {'title': title, 'tags': tags}}
                newData.update(jsonData)
                jsonData = newData.copy()

                with open('./js/posturl.json', 'w', encoding='utf-8') as f:
                    json.dump(jsonData, f)
                print('Success: 更新成功! (文章順序已變更)')

            print('Success: 已更新 {}.html 檔案!'.format(file))


def delete_article(file):
    answer = input('是否刪除檔案 (N/y): ')
    if not (answer == 'Y' or answer == 'y'):
        print('Warning: 選擇不刪除!')

    else:
        if os.path.isfile('./article/post/{}.md'.format(file)):
            os.remove('./article/post/{}.md'.format(file))
            print('Success: 已刪除 {}.md 檔案!'.format(file))

        else:
            print('Warning: {}.md 檔案不存在!'.format(file))

        if os.path.isfile('./post/{}.html'.format(file)):
            os.remove('./post/{}.html'.format(file))

            with open('./js/posturl.json', 'r', encoding='utf-8') as f:
                jsonData = json.load(f)

            if (file + '.html') in jsonData:
                del jsonData[file + '.html']

            with open('./js/posturl.json', 'w', encoding='utf-8') as f:
                json.dump(jsonData, f)

            print('Success: 已刪除 {}.html 檔案!'.format(file))

        else:
            print('Warning: {}.html 檔案不存在!'.format(file))

        print('Success: 執行完成!')


def about():
    if not os.path.isfile('./article/page/about.md'):
        print('Warning: about.md 檔案不存在!')

    else:
        with open('./article/page/about.md', 'r', encoding='utf-8') as f:
            preText = f.readlines()
            for line in range(len(preText)):
                if preText[line] == '```html\n':
                    index = line
                    while preText[index + 1] != '```\n':
                        index += 1
                        preText[index] = '    ' + preText[index]

        with open('./article/page/about.md', 'w', encoding='utf-8') as f:
            for line in preText:
                f.write(line)

        with open('./article/page/about.md', 'r', encoding='utf-8') as f:
            f.readline()
            f.readline()
            f.readline()
            title = 'About'
            text = f.read()
            html = markdown2.markdown(text).split('\n')

        for line in range(len(html)):
            if html[line].startswith('<p><code>'):
                language = html[line].split('<p><code>')[1].strip()
                html[line] = '<pre><code class="language-{} line-numbers">'.format(language)

            if html[line].endswith('</code></p>'):
                html[line] = '</code></pre>'

            if html[line].startswith('<p><img') and html[line].endswith('></p>'):
                c1 = html[line].find('"', 0)
                c2 = html[line].find('"', c1 + 1)
                c3 = html[line].find('"', c2 + 1)
                c4 = html[line].find('"', c3 + 1)
                html[line] = '<figure>' + \
                             '<img src="{}" alt="{}">'.format(html[line][c1+1:c2], html[line][c3+1:c4]) + \
                             '<figcaption>{}</figcaption>'.format(html[line][c3+1:c4]) + \
                             '</figure>'

        for line in range(len(html)):
            if html[line] == '<pre><code class="language-html line-numbers">':
                index = line
                while html[index + 1] != '</code></pre>':
                    index += 1
                    html[index] = html[index][4:]

        index = 0
        while index < len(html):
            if not (html[index].startswith('<pre><code class="language-') and html[index].endswith('line-numbers">')):
                index +=1
            else:
                html[index] += html[index + 1]
                del html[index + 1]

        html = '\n'.join(html)
        html = htmlAbout + htmlAfter.replace('PageArticle', html)

        with open('./page/about.html', 'w', encoding='utf-8') as f:
            f.write(html)

        with open('./article/page/about.md', 'r', encoding='utf-8') as f:
            preText = f.readlines()
            for line in range(len(preText)):
                if preText[line] == '```html\n':
                    index = line
                    while preText[index + 1] != '```\n':
                        index += 1
                        preText[index] = preText[index][4:]

        with open('./article/page/about.md', 'w', encoding='utf-8') as f:
            for line in preText:
                f.write(line)

        print('Success: 已更新 about.html 檔案!')


if __name__ == '__main__':
    print('所有的服務項目: 1. 新增草稿  2. 新增文章  3. 更新文章  4. 刪除文章  5. About')
    choose = input('請選擇服務項目: ')
    file = input('請輸入檔案名稱: ')
    print('------------------------------------------------------------------- ')

    if choose == '1':
        new_draft(file)

    elif choose == '2':
        add_article(file)

    elif choose == '3':
        update_article(file)

    elif choose == '4':
        delete_article(file)

    elif choose == '5':
        about()

    else:
        print('Warning: 程式結束!')

    print('------------------------------------------------------------------- ')
