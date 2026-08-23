FROM oven/bun:1 AS builder
WORKDIR /app
COPY package.json build-site.ts ./
COPY templates ./templates
RUN bun run build

FROM oven/bun:1 AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY serve.ts .
EXPOSE 3000
CMD ["bun", "serve.ts"]
