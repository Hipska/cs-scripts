# Mailchimp DMP script
mailchimp csv export: https://docs.google.com/spreadsheets/d/1ArDqAQuEE0wLu1q6Lyayql2kSbGcnJ5LxGhmsyZp4Jo/edit?usp=sharing

## GOALS
- [x] get the export into mailchimp
- [x] overview of possible tags in mailchimp
- [ ] sync mailchimp and mongo (cs)
- [ ] cron on daily basis
- [ ] keep track of changes (events) -> daily raport
- [ ] modular code -> extend to DMP in later stage

## Model
- firstname
- lastname
- email
- tags (csv)

## Caveats
### Mongo
- new added
- tages added

### Mailchimp
- user can unsubscribe
- manually added -> clean duplicates
