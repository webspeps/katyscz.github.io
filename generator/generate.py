import datetime
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from dataclasses import dataclass

PATH_TO_TEMPLATES = Path('TEMPLATES/')
PATH_TO_RESOURCES = Path('RESOURCES/')
PATH_TO_OUTPUT = Path('../docs/')
URL_ROOT = "https://katys.cz/"

link_to_homepage = "index.html"  # TODO: always / in production
html_file_suffix = ".html"


@dataclass()
class Page(object):
    title: str
    keywords: str
    description: str
    content_file: str
    url: str
    language: str
    last_mod: datetime.datetime
    phone: str = '+420 603 217 867'
    email: str = 'katys@katys.cz'

    def keys(self):
        """Get keys that allows conversion of this class to dictionary.

        Returns:
            List[str]: List of the keys to be passed to template.
        """
        return ['title', 'keywords', 'description', 'url', 'content_file',
                'language', 'phone', 'email']

    def __getitem__(self, key):
        """Allows conversion of this class to dictionary.
        """
        return getattr(self, key)

    def generate_site(self):
        with open(PATH_TO_TEMPLATES.joinpath('page.html')) as tem_han:
            template = Environment(
                loader=FileSystemLoader(PATH_TO_TEMPLATES)
            ).from_string(tem_han.read())
            html_str = template.render(
                **dict(self),
                link_to_homepage=link_to_homepage
            )
            return html_str

    @property
    def absolute_url(self):
        if self.url != 'index':
            return URL_ROOT + self.url + html_file_suffix
        return URL_ROOT

    @property
    def last_modified(self):
        if self.last_mod is None:
            return None
        return self.last_mod.strftime('%Y-%m-%d')


unified_description = "Vyrábíme atypický nábytek dle návrhů vytvořených zákazníkem, bytovým designérem nebo námi, dále kuchyně na míru, interiérové dveře, schodiště a další."
unified_keywords = "Katys, Truhlářství, Nábytek, Dřevovýroba, Liberec"

pages = [
    Page(title="Domů",
         keywords=unified_keywords,
         description=unified_description,
         url="index",
         content_file='page_home.html',
         language="cs",
         last_mod=datetime.datetime(2020, 12, 17)
         ),
    Page(title="Reference",
         keywords=unified_keywords,
         description=unified_description,
         url="reference",
         content_file='page_reference.html',
         language="cs",
         last_mod=datetime.datetime(2020, 12, 17)
         ),
    *(
        Page(title="Okna",
             keywords=unified_keywords,
             description=unified_description,
             url="okna",
             content_file='page_okna.html',
             language="cs",
             last_mod=datetime.datetime(2020, 12, 17)
             ),
        Page(title="Vchodové dveře",
             keywords=unified_keywords,
             description=unified_description,
             url="vchodove-dvere",
             content_file='page_vchodove_dvere.html',
             language="cs",
             last_mod=datetime.datetime(2020, 12, 17)
             ),
        Page(title="Interiérové dveře",
             keywords=unified_keywords,
             description=unified_description,
             url="interierove-dvere",
             content_file='page_interierove_dvere.html',
             language="cs",
             last_mod=datetime.datetime(2020, 12, 17)
             ),
        Page(title="Zimní zahrady",
             keywords=unified_keywords,
             description=unified_description,
             url="zimni-zahrady",
             content_file='page_zimni_zahrady.html',
             language="cs",
             last_mod=datetime.datetime(2020, 12, 17)
             ),
        Page(title="Interiéry",
             keywords=unified_keywords,
             description=unified_description,
             url="interiery",
             content_file='page_interiery.html',
             language="cs",
             last_mod=datetime.datetime(2020, 12, 17)
             ),
        Page(title="Kuchyně",
             keywords=unified_keywords,
             description=unified_description,
             url="kuchyne",
             content_file='page_kuchyne.html',
             language="cs",
             last_mod=datetime.datetime(2020, 12, 17)
             ),
        Page(title="Nábytek",
             keywords=unified_keywords,
             description=unified_description,
             url="nabytek",
             content_file='page_nabytek.html',
             language="cs",
             last_mod=datetime.datetime(2020, 12, 17)
             ),
        Page(title="Stavební truhlářství",
             keywords=unified_keywords,
             description=unified_description,
             url="stavebni-truhlarstvi",
             content_file='page_stavebni_truhlarstvi.html',
             language="cs",
             last_mod=datetime.datetime(2020, 12, 17)
             ),
        Page(title="Stoly a židle",
             keywords=unified_keywords,
             description=unified_description,
             url="stoly-a-zidle",
             content_file='page_stoly_a_zidle.html',
             language="cs",
             last_mod=datetime.datetime(2020, 12, 17)
             ),
      ),
    Page(title="Zelená úsporám",
         keywords=unified_keywords,
         description=unified_description,
         url="zelena-usporam",
         content_file='page_zelena_usporam.html',
         language="cs",
         last_mod=datetime.datetime(2020, 12, 17)
         ),
    Page(title="Fotogalerie",
         keywords=unified_keywords,
         description=unified_description,
         url="fotogalerie",
         content_file='page_fotogalerie.html',
         language="cs",
         last_mod=datetime.datetime(2020, 12, 17)
         ),
    Page(title="Certifikáty",
         keywords=unified_keywords,
         description=unified_description,
         url="certifikaty",
         content_file='page_certifikaty.html',
         language="cs",
         last_mod=datetime.datetime(2020, 12, 17)
         ),
    Page(title="Kontakt",
         keywords=unified_keywords,
         description=unified_description,
         url="kontakt",
         content_file='page_kontakt.html',
         language="cs",
         last_mod=datetime.datetime(2020, 12, 17)
         )
]

# Remove all existing resources
if PATH_TO_OUTPUT.exists():
    shutil.rmtree(PATH_TO_OUTPUT)

# Create new dir
PATH_TO_OUTPUT.mkdir()

for page in pages:
    content = page.generate_site()
    with PATH_TO_OUTPUT.joinpath(page.url + html_file_suffix).open('w') as fp:
        fp.write(content)

# Copy resources
shutil.copytree(PATH_TO_RESOURCES, PATH_TO_OUTPUT, dirs_exist_ok=True)

# Generate resource map:
with open(PATH_TO_TEMPLATES.joinpath('site_map.xml')) as tem_han:
    template = Environment(
        loader=FileSystemLoader(PATH_TO_TEMPLATES)
    ).from_string(tem_han.read())
    html_str = template.render(
        sites=pages
    )
    with PATH_TO_OUTPUT.joinpath('sitemap.xml').open('w') as f_xml:
        f_xml.write(html_str)

robots_txt_content = f"""User-agent: *
Allow: /
Sitemap: {URL_ROOT}sitemap.xml"""
with PATH_TO_OUTPUT.joinpath('robots.txt').open('w') as robots_txt_h:
    robots_txt_h.write(robots_txt_content)
