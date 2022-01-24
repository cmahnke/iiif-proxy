IIIF Proxy
==========

A content rewriting Proxy for IIIF

The current implementation also acts as proxy for two IIIF service of the University of Göttingen.

# Downloading

```
git clone --recurse-submodules https://github.com/cmahnke/iiif-proxy.git
```

## Building

```
docker-compose build
```


# Running

```
 docker-compose up
```


# TODO

## Infrastructure

  * Finish integration of Letsencrypt
    * Test SSL
  * Finish Helm Chart

## Functionality
  * Implement IIIF presentation manifest rewrite


# Links to try

* https://images.sub.uni-goettingen.de/iiif/image/gdz:DE-611-HS-3461927:00000001/info.json
