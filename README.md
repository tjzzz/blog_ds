本博客是基于mkdocs搭建的静态博客，通过obsidian的进行markdown的文档书写，然后用mkdocs+github-pages进行发布，
模版参考 https://github.com/Jackiexiao/foam-mkdocs-template

具体使用方式可以参看 mkdocs文档或者上述参考模版

最终生成的博客地址： https://tjzzz.github.io/blog_ds/



## Usage：Deploy to github page

1. fork this repository , go to repo `setting -> action -> workflow permissions` change to `read and write permissions`
2. copy ` .github mkdocs.yml requirements.txt` to your repo, and create `docs` directory 
3. add your documents to `docs` , `docs/index.md` is the main page of the website
4. open `mkdocs.yml`, modify `site_name` to your website name, this file is the setting of website, visit link below to get more information(for example, you may want to change language to en)
* [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)
* [mkdocs](https://www.mkdocs.org/user-guide/configuration/)
5. push to github, ps: before push to github, you may want to preview your website locally, please view [deploy locally](#deploy-locally)
6. go to github setting, open github page, choose `gh-pages` branch, wait a moment, then visit `http://<your-github-username.github.io/<your-repo>`, for example:`jackiexiao.github.io/blog/`
7. Done! That's all! Have fun!

Thx to `Github Action`, it make deploy a blog so easy, all you need todo is modify and push your file

## Deploy Locally

The simplest way: Enter your local repo directory, make sure your python > 3.6
```
pip install -U -r requirements.txt
mkdocs serve 
```
Then visit `http://127.0.0.1:8000/`

## Support syntax
This template will convert roam/obsidian/foam like links to web support links

| origin                  | convert                             |
| ----------------------- | ----------------------------------- |
| `[Git Flow](git_flow.md)` | `[Git Flow](../software/git_flow.md)` |
| `[[Git Flow]]`            | `[Git Flow](../software/git_flow.md)` |
| `![[image.png]]`           | `![image.png](../image/imag.png)`      |
| `[[#Heading identifiers]]` | `[Heading identifiers in HTML](#heading-identifiers-in-html)`
| ` [[Git Flow#Heading]]` | `[Git Flow](../software/git_flow.md#heading)` |

