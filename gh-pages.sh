#!/bin/bash

cd pages

email=$(git config user.email)
name=$(git config user.name)
url=$(git remote get-url origin)

git init
git config user.email $email
git config user.name $name
git remote add origin $url
git checkout -b gh-pages
git add .
git commit -m "Deploy gh-pages"
git push -f origin gh-pages

rm -rf .git
