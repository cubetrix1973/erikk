#!/bin/bash
fswatch -o /Users/kike/Desktop/proyectos/erikk --exclude='.git' | while read f; do
  rsync -az --exclude='.git' /Users/kike/Desktop/proyectos/erikk/ root@187.124.9.54:/home/dev/projects/erikk/
  ssh root@187.124.9.54 'nginx -s reload'
  echo "✓ Sincronizado $(date)"
done
