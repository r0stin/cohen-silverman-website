# Cohen & Silverman Law Firm website

A complete static website (18 pages): plain HTML, CSS and JavaScript. No framework, nothing to install, and it runs on any web host.

## Pages

| Page | File |
|---|---|
| Home | `index.html` |
| Practice areas overview | `practice-areas.html` |
| Debt Recovery | `debt-recovery.html` |
| Harassment | `harassment.html` |
| Extortion & Blackmail | `extortion-blackmail.html` |
| Restraining Orders | `restraining-orders.html` |
| Defamation | `defamation.html` |
| Fraud & Civil Theft | `fraud-civil-theft.html` |
| Our Lawyers (with full bios) | `attorneys.html` |
| About | `about.html` |
| Contact / book a consultation | `contact.html` |
| Guides (index) | `guides.html` |
| Guide: money owed | `guide-unpaid-debt.html` |
| Guide: blackmail and sextortion | `guide-sextortion-first-24-hours.html` |
| Guide: restraining orders | `guide-restraining-orders.html` |
| Guide: documenting harassment | `guide-documenting-harassment.html` |
| Legal notices & privacy | `legal.html` |
| Page not found | `404.html` |

To preview, double-click `index.html`.

## Making changes

The pages are generated from `_source/`. Firm details, practice areas and lawyer bios live in `_source/build.py`, and the guide articles live in `_source/guides.py`. Hand-written pages (home, about, contact, legal, 404) are in `_source/pages/`.

After editing, rebuild:

```
python _source/build.py
```

The script rewrites every page, so the header, footer and contact details stay identical on all of them. Don't edit the generated `.html` files in the main folder directly, because the next build will overwrite them.

## Before you launch

Placeholders and assumptions that must be checked:

1. **Contact details.** Phone `(905) 604-7662` is set. Email `intake@cohensilverman.com` is a placeholder until that mailbox exists, and the address and hours are placeholders too. Change them in `FIRM` at the top of `_source/build.py`, then rebuild.
2. **Contact form.** No form service is connected yet, so the form opens the visitor's email app with their message filled in. To receive submissions directly, create a form with a service such as Formspree, paste its URL into `form_endpoint` in `FIRM`, and rebuild.
3. **Headshots.** Done. The four photos are in `assets/img/team/` (`benjamin-cohen.jpg`, `joshua-silverman.jpg`, `rebecca-anderson.jpg`, `noah-katz.jpg`). To change one, replace the file with a new portrait photo of the same name (about 3:4 or 4:5, at least 768 px wide) and rebuild.
4. **Lawyer titles and bios.** Rebecca Anderson is listed as *Partner* and Noah Katz as *Associate*. Bios describe each lawyer's focus but contain no education, bar admissions or years of practice. Confirm the titles and add credentials.
5. **Service promises.** Check that you're happy to commit to: contact "usually within one business day", evening appointments, fixed, hourly and contingency fee options (About page), and fees confirmed in writing.
6. **Jurisdiction.** The copy is location-neutral. It mentions 911 as the emergency number, limitation periods "as short as two years", and "restraining order (in some places a protection order or peace bond)". Adjust these for where you practice, and check the site against your law society's or bar's advertising rules.
7. **Guides.** The four guides are general information written to be location-neutral. Have a lawyer at the firm review them before publishing, and update the date in `_source/guides.py` when they change.
8. **Legal page.** The disclaimer, privacy policy and terms are a sound starting point, but have them reviewed for your jurisdiction.
9. **Domain.** Done. The site is set up for `https://cohensilverman.com` (`SITE_URL` in `_source/build.py`). The build also writes `sitemap.xml`, `robots.txt` and `CNAME`.

## Hosting

The site is hosted on GitHub Pages. Every push to the `main` branch publishes it automatically through `.github/workflows/deploy.yml`, which uploads only the public files (the pages, `assets/`, `CNAME`, `robots.txt` and `sitemap.xml`). `_source/`, `.claude/` and this README are not published.

To update the live site: edit the source, run `python _source/build.py`, then commit and push.

DNS for `cohensilverman.com` at your domain registrar:

| Type | Name | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | r0stin.github.io |

Once DNS has propagated, tick **Enforce HTTPS** in the repository's Settings > Pages.

Fonts (Source Serif 4 and Source Sans 3 from Google Fonts), icons (Phosphor, via unpkg) and photos (Unsplash, free license) load from their own servers.

## Brand assets

`assets/img/brand/` holds transparent cut-outs of every logo in your kit, in navy and in white (PNG for print and documents, WebP for the web). Also included: favicons, an app icon, a social sharing image and the original logo kit.
