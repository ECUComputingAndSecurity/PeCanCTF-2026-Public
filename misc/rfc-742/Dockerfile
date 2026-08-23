FROM alpine:3.22.4 AS build

RUN echo "@testing https://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && apk add --no-cache finger@testing

RUN	addgroup -S finger && \ 	
	adduser -g "Joshua" -D raahguu -G finger && \
	printf "...Make Challenges...\n...Write Flags..." > /home/raahguu/.plan && \
	adduser -g "Xanarto Xanarto" -D xanarto -G finger && \
	printf "1.Refine my coding skills\n2.Figure out how to run GIMP in the browser" > /home/xanarto/.plan && \
	adduser -g "Morris Worm" -D morris -G finger && \
	printf "Infect Everything\nIncluding: pecan{p0k3_p0k3_d07_do7_do7_p0k3_p0k3}" > /home/morris/.plan

FROM scratch

COPY --from=build /usr/bin/fingerd /usr/bin/fingerd
COPY --from=build /lib/ld-musl-x86_64.so.1 /lib/
COPY --from=build /home /home
COPY --from=build /etc/passwd /etc/passwd
COPY --from=build /etc/group /etc/group

EXPOSE 79
CMD ["fingerd", "-a",  "0.0.0.0"]
